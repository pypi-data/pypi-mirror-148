import attr
import collections
import datetime
import dateutil
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import json
from pathlib import Path
import time
from typing import Optional
from urllib.error import HTTPError

from ..base import Contact
from ..connect import Connection
from ..addresses import Address
from ..types import PhoneType, ContactType
from ..utils import (
    _rowget,
    _str_not_none,
    _date_to_ymd,
    _make_dict_from_list,
    _strip_bad_chars,
)
from ..phones import Phone
from ..addresses import Address

DEFAULT_SCOPES = ['https://www.googleapis.com/auth/contacts']
API_NAME = "people"
API_VERSION = "v1"
PERSON_FIELDS = str(
    "names,addresses,biographies,birthdays,calendarUrls,clientData,"
    "emailAddresses,events,genders,metadata,miscKeywords,nicknames,occupations,"
    "organizations,phoneNumbers,photos,relations,urls,userDefined"
)

@attr.s(auto_attribs=True)
class GoogleConnection(Connection):
    token_file_or_path: Optional[str] = ""
    client_secrets_file: Optional[str] = None

    def _setup_service(self):
        creds = None
        if isinstance(self.token_file_or_path, dict):
            creds = Credentials.from_authorized_user_info(
                self.token_file_or_path
            )
            token_path = None
        else:
            token_path = Path(self.token_file_or_path)
            if token_path.exists():
                creds = Credentials.from_authorized_user_file(
                    token_path, DEFAULT_SCOPES
                )
        if creds is None:
            try:
                client_secrets_path = Path(self.client_secrets_file)
                if not client_secrets_path.exists():
                    raise TypeError()
            except TypeError:
                raise Exception(
                    "must provide valid client_secrets_file "
                    "if token_file does not exist"
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_path,
                DEFAULT_SCOPES,
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        if token_path is not None:
            with token_path.open("w") as tf:
                tf.write(creds.to_json())
        return build(API_NAME, API_VERSION, credentials=creds)

    def __attrs_post_init__(self):
        self._service = self._setup_service()

    @classmethod
    def contact_type(cls):
        return GoogleContact

    @classmethod
    def dict_to_contact(cls, d, **kwargs):
        return GoogleContact.from_api(d, **kwargs)

    @classmethod
    def contact_to_dict(cls, c, include_etag=True, **kwargs):
        return GoogleContact.to_api(c, include_etag=include_etag, **kwargs)

    def _get_batch(self, id):
        responses = self._service.people().getBatchGet(
                resourceNames=id,
                personFields=PERSON_FIELDS,
            ).execute()
        return self._convert_to_contact_and_drop_none(
            responses["responses"]
        )

    def _get_raw(self, id):
        return self._service.people().get(
            resourceName=id,
            personFields=PERSON_FIELDS,
        ).execute()

    def get(self, id, convert=True):
        if ( isinstance(id, collections.Iterable)
               and not isinstance(id, str)):
            return self._get_batch(id)
        vals = self._get_raw(id)
        if convert:
            return self._convert_to_contact_and_drop_none(vals)
        return vals


    def get_by_name(self, fn, ln, convert=True):
        results = self._service.people().searchContacts(
            pageSize=100,
            query=f"{fn} {ln}",
            readMask=PERSON_FIELDS,
        ).execute()
        vals = results["results"]
        if len(vals) == 100:
            raise Exception(
                "Error: found too many results (>100) when looking for "
                f"contact with name {fn} {ln}."
            )
        if convert:
            return self._convert_to_contact_and_drop_none(vals)
        return vals

    @staticmethod
    def _strip_non_create_fields(d, strip_etag=True):
        if "resourceName" in d:
            del d["resourceName"]
        # photos is read only
        if "photos" in d:
            del d["photos"]
        if "etag" in d and strip_etag:
            del d["etag"]

    def create(self, d):
        GoogleConnection._strip_non_create_fields(d)
        response = self._service.people().createContact(
            body=d,
            personFields=PERSON_FIELDS,
        ).execute()
        if "resourceName" in response:
            return response["resourceName"]
        else:
            return None

    def delete(self, c):
        self._service.people().deleteContact(
            resourceName=c.gcid
        ).execute()

    def _get_updated_fields(self, c):
        curd = self.contact_to_dict(self.get(c.gcid)[0], include_etag=True)
        chgd = self.contact_to_dict(c, include_etag=True)
        output_keys = []
        for k in chgd.keys():
            if chgd[k] != curd.get(k,None):
                output_keys.append(k)
        return { k:chgd[k] for k in output_keys }

    def _do_update(self, c, fields_to_update):
        update_fields = self._get_updated_fields(c)
        GoogleConnection._strip_non_create_fields(update_fields, strip_etag=False)
        etag = c._etag
        if "etag" in update_fields:
            etag = update_fields["etag"]
        old_update_fields = dict(update_fields)
        update_person_fields = ",".join(
            [k for k in update_fields.keys() if k != "etag"]
        )
        if fields_to_update is not None:
            update_person_fields=fields_to_update
        if update_person_fields is None or len(update_person_fields) == 0:
            return
        body_dict = self.contact_to_dict(c, include_etag=True)
        body_dict["etag"] = etag
        self._service.people().updateContact(
            body=body_dict,
            resourceName=c.gcid,
            updatePersonFields=update_person_fields,
            personFields=PERSON_FIELDS,
        ).execute()

    def update(self, c, fields_to_update=None):
        try:
            self._do_update(c, fields_to_update)
        except HttpError as e:
            if str(e).lower().find("etag is different") >= 0:
                self._do_update(c, fields_to_update)
            else:
                raise

    def list(self, page_size=1000):
        next_page = ""
        last_page = None
        output = []
        while True:
            d = self._service.people().connections().list(
                pageSize=page_size,
                requestSyncToken=False,
                resourceName="people/me",
                pageToken=next_page,
                personFields=PERSON_FIELDS,
            ).execute()
            output.extend(d.get("connections",[]))
            last_page = next_page
            next_page = d.get("nextPageToken")
            if next_page is None or len(next_page) == 0:
                break
            if last_page == next_page:
                raise Exception(
                    "Found next/last pages same "
                    f"({last_page}=={next_page})"
                )
        return self._convert_to_contact_and_drop_none(output)

    def query(self, query):
        results = self._service.people().searchContacts(
            pageSize=1000,
            query=query,
            readMask=PERSON_FIELDS,
        ).execute()
        vals = results["results"]
        if len(vals) == 1000:
            raise Exception(
                "Error: found too many results (>1000) when looking for "
                f"contact based on query {query}"
            )
        return self._convert_to_contact_and_drop_none(vals)

    def create_batch(self, batch):
        contact_batch = []
        for d in batch:
            GoogleConnection._strip_non_create_fields(d)
            contact_batch.append(
                {"contactPerson": d}
            )
        params = { "contacts": contact_batch, "readMask": "names"  }
        results = self._service.people().batchCreateContacts(
            body=params,
        ).execute()
        if "createdPeople" not in results:
            return []
        return [r["person"]["resourceName"] for r in results["createdPeople"]]

    # don't use batchUpdateContacts - has some bad properties unless
    # doing a homogenous update of the same fields across many contacts, which
    # we don't want to pigeonhole users into - rather take the performance hit
    def update_batch(self, batch):
        for c in batch:
            self.update(c)

class GoogleAddress(Address):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_api(cls, row, ctype=None):
        item = GoogleAddress()
        addresses = {x.get("formattedType","Unknown").replace(" ","") : x for x in row.get('addresses', {})}
        if "Home" not in addresses and "Unknown" in addresses:
            addresses["Home"] = addresses["Unknown"]
        addr_dict = addresses.get(ctype.value, {})

        streetaddr = _strip_bad_chars(_rowget(addr_dict, "streetAddress"))
        if streetaddr is not None:
            streetaddrs = streetaddr.split("\n")
            item.addr1 = streetaddrs[0]
            if len(streetaddrs) > 1:
                item.addr2 = streetaddrs[1]

        addr2 = _strip_bad_chars(_rowget(addr_dict, "extendedAddress"))
        if addr2 is not None:
            if item.addr2 is not None:
                item.addr2 += addr2
            else:
                item.addr2 = addr2
        item.city  = _strip_bad_chars(_rowget(addr_dict, "city"))
        item.region = _strip_bad_chars(_rowget(addr_dict, "region"))
        item.country = _strip_bad_chars(_rowget(addr_dict, "country"))
        item.zip = _strip_bad_chars(_rowget(addr_dict, "postalCode"))
        item._type = ctype
        item.adjust_zip()
        item.adjust_country()
        return item

    @classmethod
    def to_api(cls, addr, **kwargs):
        d = {}
        if addr is None or addr.countfields() == 0:
            return d
        d["type"] = addr._type.value
        d["streetAddress"] = _strip_bad_chars(_str_not_none(getattr(addr, "addr1", "")))
        d["extendedAddress"] = _strip_bad_chars(_str_not_none(getattr(addr, "addr2", "")))
        d["city"] = _strip_bad_chars(_str_not_none(getattr(addr, "city", "")))
        d["region"] = _strip_bad_chars(_str_not_none(getattr(addr, "region", "")))
        d["postalCode"] = _strip_bad_chars(_str_not_none(getattr(addr, "zip", "")))
        d["country"] = _strip_bad_chars(_str_not_none(getattr(addr, "country", "")))
        return d

class GoogleContact(Contact):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def ids(cls):
        return ["gcid"]

    @classmethod
    def multi_to_list(cls, s):
        if isinstance(s, list):
            return s
        if isinstance(s, str):
            return [ subs.strip() for subs in s.split(";") ]
        raise Exception(f"Invalid input {s}, not list or string")

    @classmethod
    def to_api(cls, c, include_etag=True, **kwargs):
        d = {}
        d["resourceName"] = _strip_bad_chars(c._id)

        if include_etag:
            d["etag"] = _strip_bad_chars(c._etag)

        names = {}
        if c.fn is not None:
            names["givenName"] = _strip_bad_chars(c.fn)
        if c.ln is not None:
            names["familyName"] = _strip_bad_chars(c.ln)
        if c.mn is not None:
            names["middleName"] = _strip_bad_chars(c.mn)
        if c.prefix is not None:
            names["honorificPrefix"] = _strip_bad_chars(c.prefix)
        if c.suffix is not None:
            names["honorificSuffix"] = _strip_bad_chars(c.suffix)
        d["names"] = names

        nicknames = []
        if c.nn is not None:
            nicknames.append({"value": _strip_bad_chars(c.nn)})
        d["nicknames"] = nicknames

        addrs = []
        for addrtype in [ "haddr", "h2addr", "waddr" ]:
            addr_dict = GoogleAddress.to_api(getattr(c, addrtype))
            if len(addr_dict):
                addrs.append(addr_dict)
        d["addresses"] = addrs

        emails = []
        if c.email1 is not None:
            emails.append({"type": "Home", "value": _strip_bad_chars(c.email1)})
        if c.email2 is not None:
            emails.append({"type": "Home2", "value": _strip_bad_chars(c.email2)})
        if c.authemail is not None:
            emails.append({"type": "Authorized", "value": _strip_bad_chars(c.authemail)})
        d["emailAddresses"] = emails

        phones = []
        if c.mobilephone is not None and len(c.mobilephone):
            phones.append({"type": "Mobile", "value": _strip_bad_chars(c.mobilephone)})
        if c.mobile2phone is not None and len(c.mobile2phone):
            phones.append({"type": "Mobile2", "value": _strip_bad_chars(c.mobile2phone)})
        if c.mobile3phone is not None and len(c.mobile3phone):
            phones.append({"type": "Mobile3", "value": _strip_bad_chars(c.mobile3phone)})
        if c.otherphone is not None and len(c.otherphone):
            phones.append({"type": "Other", "value": _strip_bad_chars(c.otherphone)})
        if c.other2phone is not None and len(c.other2phone):
            phones.append({"type": "Other2", "value": _strip_bad_chars(c.other2phone)})
        if c.homephone is not None and len(c.homephone):
            phones.append({"type": "Home", "value": _strip_bad_chars(c.homephone)})
        if c.home2phone is not None and len(c.home2phone):
            phones.append({"type": "Home2", "value": _strip_bad_chars(c.home2phone)})
        if c.workphone is not None and len(c.workphone):
            phones.append({"type": "Work", "value": _strip_bad_chars(c.workphone)})
        if c.work2phone is not None and len(c.work2phone):
            phones.append({"type": "Work2", "value": _strip_bad_chars(c.work2phone)})
        if c.asstphone is not None and len(c.asstphone):
            phones.append({"type": "Assistant", "value": _strip_bad_chars(c.asstphone)})
        if c.mainphone is not None and len(c.mainphone):
            phones.append({"type": "Main", "value": _strip_bad_chars(c.mainphone)})
        if c.workfax is not None and len(c.workfax):
            phones.append({"type": "Fax", "value": _strip_bad_chars(c.workfax)})
        d["phoneNumbers"] = phones

        bios = []
        if c.notes is not None:
            bios.append({"value": c.notes})
        d["biographies"] = bios

        birthdays = []
        if c.birthday is not None:
            dt = _date_to_ymd(c.birthday)
            birthdays.append({
                "text": c.birthday,
                "date": { "day": dt[2], "year": dt[0], "month": dt[1] },
            })
        d["birthdays"] = birthdays

        events = []
        if c.anniversary is not None:
            dt = _date_to_ymd(c.anniversary)
            events.append({
                "type": "Anniversary",
                "date": { "day": dt[2], "year": dt[0], "month": dt[1] },
            })
        d["events"] = events

        urls = []
        if c.url is not None:
            urls.append({"value": c.url})
        d["urls"] = urls

        organizations = []
        if c.org is not None or c.jobtitle is not None or c.company is not None:
            org = {}
            org["name"] = c.org
            if c.org is None:
                if c.company is not None:
                    org["name"] = _strip_bad_chars(c.company)
                else:
                    org["name"] = "Unknown"
            if c.jobtitle is not None:
                org["title"] = _strip_bad_chars(c.jobtitle)
            organizations.append(org)
        d["organizations"] = organizations

        relations = []
        if c.spouse is not None:
            relations.append({"type": "Spouse", "person": _strip_bad_chars(c.spouse)})
        if c.child1 is not None:
            relations.append({"type": "Child1", "person": _strip_bad_chars(c.child1)})
        if c.child2 is not None:
            relations.append({"type": "Child2", "person": _strip_bad_chars(c.child2)})
        if c.child3 is not None:
            relations.append({"type": "Child3", "person": _strip_bad_chars(c.child3)})
        if c.child4 is not None:
            relations.append({"type": "Child4", "person": _strip_bad_chars(c.child4)})
        d["relations"] = relations

        photos = []
        if c.photo is not None:
            photos.append({"url": _strip_bad_chars(c.photo)})
        d["photos"] = photos

        userdef = []
        if c.title is not None:
            userdef.append({"key": "Title", "value": _strip_bad_chars(c.title)})
        if c.social is not None:
            userdef.append({"key": "Social", "value": _strip_bad_chars(c.social)})
        if c.uid is not None:
            userdef.append({"key": "UniqueID", "value": _strip_bad_chars(c.uid)})
        if c.atid is not None:
            userdef.append({"key": "AirtableID", "value": _strip_bad_chars(c.atid)})
        if c.cplusid is not None:
            userdef.append({"key": "CPlusID", "value": _strip_bad_chars(c.cplusid)})
        if c.gid is not None:
            userdef.append({"key": "OldGoogleID", "value": _strip_bad_chars(c.gid)})
        if c.gcid is not None:
            userdef.append({"key": "GoogleContactID", "value": _strip_bad_chars(c.gcid)})
        if c.altgcid is not None:
            userdef.append({"key": "AltGoogleContactID", "value": _strip_bad_chars(c.altgcid)})
        if c.customterm is not None:
            userdef.append(
                {"key": "Custom Additional Mailing Term", "value": _strip_bad_chars(c.customterm)}
            )
        if c.customrepl is not None:
            userdef.append(
                {"key": "Custom Replacement Mailing Term", "value": _strip_bad_chars(c.customrepl)}
            )
        if c.source is not None:
            userdef.append({"key": "Source", "value": _strip_bad_chars(c.source)})
        if c.spouseid is not None:
            userdef.append({"key": "SpouseID", "value": _strip_bad_chars(c.spouseid)})
        if c.category is not None and len(c.category):
            userdef.append({"key": "Category", "value": ";".join(c.category)})
        if c.holidaylists is not None and len(c.holidaylists):
            userdef.append(
                {"key": "HolidayLists", "value": ";".join(c.holidaylists)})
        if c.isholiday is not None:
            userdef.append({
                "key": "IsHoliday",
                "value": str(c.isholiday)
            })
        if c.isandfamily is not None:
            userdef.append({
                "key": "Use And Family Syntax",
                "value": str(c.isandfamily),
            })
        if c.isworkmain is not None:
            userdef.append({
                "key": "Use Work Address As Main",
                "value": str(c.isworkmain),
            })
        if c.isspouse is not None:
            userdef.append({
                "key": "Treat As Spouse (default yes)",
                "value": str(c.isspouse)
            })
        if c.iscombosurname is not None:
            userdef.append({
                "key": "Use Combination Surname For Family (default no)",
                "value": str(c.iscombosurname),
            })
        if c.isspousemain is not None:
            userdef.append({
                "key": "Use Spouse as Main Surname (default no)",
                "value": str(c.isspousemain)
            })
        if c.linkedin is not None:
            userdef.append({"key": "LinkedIn", "value": str(c.linkedin)})
        if c.created is not None:
            userdef.append({"key": "Created", "value": str(c.created)})
        if c.lmod is not None:
            userdef.append({"key": "LastModified", "value": str(c.lmod)})
        d["userDefined"] = userdef
        return d

    @classmethod
    def from_api(cls, datarow, **kwargs):
        c = GoogleContact()
        c._fs = "Google"
        row= datarow.get('person')
        if row is None:
            if datarow.get("resourceName") is None:
                return None
            row = datarow
        c._id = row["resourceName"]
        c._etag = row.get("etag")
        nameslist = row.get("names")
        if nameslist is None or len(nameslist) == 0:
            return None
        names = nameslist[0]
        c.ln = _rowget(names, "familyName")
        if c.ln is not None:
            c.ln = c.ln.strip()
        c.fn = _rowget(names,'givenName')
        if c.fn is not None:
            c.fn = c.fn.strip()
        c.mn = _rowget(names, 'middleName')
        if c.mn is not None:
            c.mn = c.mn.strip()
        c.prefix = _rowget(names, "honorificPrefix")
        if c.prefix is not None:
            c.prefix = c.prefix.strip()
        c.suffix = _rowget(names, "honorificSuffix")
        if c.suffix is not None:
            c.suffix = c.suffix.strip()

        nnameslist = row.get("nicknames")
        nname = {}
        if nnameslist is not None and len(nnameslist) > 0:
            nname = nnameslist[0]
        c.nn = _rowget(nname, 'value')
        if c.nn is not None:
            c.nn = c.nn.strip()

        if ( (c.ln is None or not len(c.ln) ) and
             (c.fn is None or not len(c.fn) ) ):
             return None

        c.waddr = GoogleAddress.from_api(row, ctype=ContactType.Work)
        c.haddr = GoogleAddress.from_api(row, ctype=ContactType.Home)
        c.h2addr = GoogleAddress.from_api(row, ctype=ContactType.Home2)
        if c.h2addr == c.haddr:
            c.h2addr = GoogleAddress()

        emails_dict = _make_dict_from_list(
            row.get('emailAddresses', {}), keyname="formattedType"
        )
        emails = []
        if c.ln == "Asher" and c.fn == "Scott":
            print(emails_dict)
        for _type in ["Home", "Home2", "Work", "Work2", "Other", "Other2"]:
            val = emails_dict.get(_type)
            if val is not None:
                emails.append(val)
        c.email1 = ""
        if len(emails) > 0:
            c.email1 = emails[0]
        if len(emails) > 1:
            c.email2 = emails[1]
        c.authemail = _rowget(emails_dict, "Authorized")
        if c.ln == "Asher" and c.fn == "Scott":
            print(f"e1: {c.email1} e2: {c.email2} ae: {c.authemail}")

        phones_dict = _make_dict_from_list(
            row.get('phoneNumbers', {}), keyname="formattedType", valname="value"
        )
        c.mainphone = Phone.make(
            _rowget(phones_dict, 'Main'), PhoneType.Main
        ).stringify()
        c.homephone = Phone.make(
            _rowget(phones_dict, 'Home'), PhoneType.Home
        ).stringify()
        c.workphone = Phone.make(
            _rowget(phones_dict, 'Work'), PhoneType.Work
        ).stringify()
        c.home2phone = Phone.make(
            _rowget(phones_dict, 'Home2'), PhoneType.Home2
        ).stringify()
        c.work2phone = Phone.make(
            _rowget(phones_dict, 'Work2'), PhoneType.Work2
        ).stringify()

        if c.homephone == c.home2phone:
            pass
            #c.home2phone = None
        if c.workphone == c.work2phone:
            pass
            #c.work2phone = None

        c.asstphone = Phone.make(
            _rowget(phones_dict, 'Assistant'), PhoneType.Asst
        ).stringify()
        c.mobilephone = Phone.make(
            _rowget(phones_dict, 'Mobile'), PhoneType.Mobile
        ).stringify()
        c.mobile2phone = Phone.make(
            _rowget(phones_dict, 'Mobile2'), PhoneType.Mobile2
        ).stringify()
        c.mobile3phone = Phone.make(
            _rowget(phones_dict, 'Mobile3'), PhoneType.Mobile3
        ).stringify()
        if c.mobilephone == c.mobile2phone:
            pass
            c.mobile2phone = None
        if c.mobilephone == c.mobile3phone:
            pass
            c.mobile3phone = None
        if c.mobile2phone == c.mobile3phone:
            pass
            c.mobile3phone = None

        c.otherphone = Phone.make(
            _rowget(phones_dict, 'Other'), PhoneType.Other
        ).stringify()
        c.other2phone = Phone.make(
            _rowget(phones_dict, 'Other2'), PhoneType.Other2
        ).stringify()
        if c.otherphone == c.other2phone:
            c.other2phone = None

        urls = _rowget(row, "urls")
        url = {}
        if urls is not None and len(urls) > 0:
            url = urls[0]
        c.url = _rowget(url, "value")

        photos_list = _rowget(row, 'photos')
        photo = {}
        if photos_list is not None and len(photos_list) > 0:
            photo = photos_list[0]
        c.photo = _rowget(photo, "url")

        orgs = row.get("organizations")
        org = {}
        if orgs is not None and len(orgs) > 0:
            # this could be a source of churn if the dict returned varies
            # order of orgs
            for _org in orgs:
                if "name" in _org:
                    org = _org
                    break
        c.org = _rowget(org, "name")
        c.company = c.org
        c.jobtitle = _rowget(org, "title")

        spouse = None
        children = []
        relations_dict = _make_dict_from_list(
            row.get('relations', {}), keyname="formattedType", valname="person"
        )
        c.child1 = _rowget(relations_dict, "Child1")
        c.child2 = _rowget(relations_dict, "Child2")
        c.child3 = _rowget(relations_dict, "Child3")
        c.child4 = _rowget(relations_dict, "Child4")
        c.spouse = _rowget(relations_dict, 'Spouse')

        notes_list = _rowget(row, "biographies")
        notes = {}
        if notes_list is not None and len(notes_list) > 0:
            notes = notes_list[0]
        c.notes = _rowget(notes, "value")

        events_dict = _make_dict_from_list(
            row.get('events', {}), keyname="formattedType", valname="date"
        )
        anniv = _rowget(events_dict, "Anniversary")
        c.anniversary = anniv
        if anniv is not None:
            c.anniversary = "{month:02}/{day:02}/{year:04}".format(**anniv)

        birthday_list = _rowget(row, "birthdays")
        birthday = {}
        if birthday_list is not None and len(birthday_list) > 0:
            birthday = birthday_list[0]
        c.birthday = _rowget(birthday, "text")

        userdef_dict = _make_dict_from_list(
            _rowget(row,"userDefined", []), keyname="key", valname="value"
        )
        c.title = _rowget(userdef_dict, "Title")
        c.source = _rowget(userdef_dict, 'Source')
        c.linkedin = _rowget(userdef_dict, "LinkedIn")
        c.social = _rowget(userdef_dict, 'Social')
        c.uid = str(_rowget(userdef_dict, 'UniqueID'))
        c.cplusid = _rowget(userdef_dict, "CPlusID")
        c.atid = _rowget(userdef_dict, "AirtableID")
        c.spouseid = _rowget(userdef_dict, 'SpouseID')
        c.customterm = _rowget(userdef_dict, "Custom Additional Mailng Term")
        c.customrepl = _rowget(userdef_dict, "Custom Replacement Mailing Term")
        c.gid = _rowget(userdef_dict, "OldGoogleID")
        c.gcid = c._id
        c.altgcid = _rowget(userdef_dict, "AltGoogleContactID")
        c.category = [x for x in _rowget(
                userdef_dict, "Category", "").split(";") if x]
        c.holidaylists = [x for x in _rowget(
            userdef_dict, "HolidayLists", "").split(";") if x]
        c.isandfamily = _rowget(userdef_dict, "Use And Family Syntax", None, bool)
        c.isholiday = _rowget(userdef_dict, "IsHoliday", None, bool)
        c.isworkmain = _rowget(userdef_dict, "Use Work Address As Main", None, bool)
        c.isspouse = _rowget(userdef_dict, "Treat As Spouse (default no)", None, bool)
        c.iscombosurname = _rowget(userdef_dict, "Use Combination Surname For Family (default no)", None, bool)
        c.isspousemain = _rowget(userdef_dict, "Use Spouse As Main Surname (default no)", None, bool)
        c.created = _rowget(userdef_dict, "Created")
        c.lmod = _rowget(userdef_dict, "LastModified")

        metadata = _make_dict_from_list(
            _rowget(row["metadata"],"sources",[]),keyname="type",valname="updateTime", error_on_missing=False,
        )
        c.lmoddt = dateutil.parser.isoparse(metadata["CONTACT"])
        if c.created is None:
            c.createddt = datetime.datetime(datetime.MAXYEAR, 1, 1,0,0,0, tzinfo=datetime.timezone.utc)
        else:
            c.createddt = dateutil.parser.isoparse(c.created)
        return c
