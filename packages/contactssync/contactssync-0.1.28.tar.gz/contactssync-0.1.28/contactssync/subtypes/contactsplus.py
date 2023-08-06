
import attr
import collections
import json
import requests

from ..addresses import Address
from ..base import Contact
from ..connect import Connection
from ..phones import Phone
from ..types import OptStr, PhoneType, ContactType
from ..utils import (
    _rowget,
    _tolower,
    _str_not_none,
    _date_to_ymd,
    _make_dict_from_list,
    _chunks,
)
from ..vars import (
    CPLUS_CREATE_CONTACTS_URL,
    CPLUS_UPDATE_CONTACTS_URL,
    CPLUS_SCROLL_CONTACTS_URL,
    CPLUS_SEARCH_CONTACTS_URL,
    CPLUS_DELETE_CONTACTS_URL,
    CPLUS_GET_CONTACTS_URL,
    CPLUS_REFRESH_TOKEN_URL,
)

@attr.s(auto_attribs=True)
class CPlusConnection(Connection):
    client_id: str
    client_secret: str
    refresh_token: str

    def _refresh_token(self):
        response = requests.post(
            url=CPLUS_REFRESH_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": self.client_id, "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            },
        )
        self._token = response.json()['access_token']

    def _get_header(self):
        self._refresh_token()
        return {
            "Content-Type": "application/json",
            f"Authorization": f"Bearer {self._token}"
        }

    def _convert_to_contact_and_drop_none(cls, ds):
        if isinstance(ds, dict) and "contacts" in ds:
            return super()._convert_to_contact_and_drop_none(ds["contacts"])
        return super()._convert_to_contact_and_drop_none(ds)

    @classmethod
    def contact_type(cls):
        return CPlusContact

    @classmethod
    def dict_to_contact(cls, d, **kwargs):
        return CPlusContact.from_api(d, **kwargs)

    @classmethod
    def contact_to_dict(cls, c, include_etag=True, **kwargs):
        return CPlusContact.to_api(c, include_etag=include_etag, **kwargs)

    def get(self, id):
        if not isinstance(id, list):
            id = [id]
        response = requests.post(
            url=CPLUS_GET_CONTACTS_URL,
            headers=self._get_header(),
            data=json.dumps({"contactIds": id})
        )
        if not response.ok:
            raise Exception(
                f"Error: code {response.status_code}, text: {response.text}"
                " could not get cplus contact {id}"
            )
        return self._convert_to_contact_and_drop_none(response.json())

    def get_by_name(self, fn, ln, etag=None):
        params = { "searchQuery": f"name:{fn} {ln}"}
        if etag is not None:
            params["searchQuery"] += f" AND etag:{etag}"
        response = requests.post(
            url=CPLUS_SEARCH_CONTACTS_URL,
            headers=self._get_header(),
            data=json.dumps(params)
        )

        if not response.ok:
            raise Exception(
                f"Error: code {response.status_code}, text: {response.text}"
                f" could not get cplus contact by name ({fn} {ln}"
            )
        d = response.json()
        if len(d) == 0:
            return []
        if "contacts" in d:
            d = d["contacts"]
        ids =  [ subd["contactId"] for subd in d ]
        # unfortunately Search returns less data than Get, so we have to do
        # this hack to get the id, then grab it via Get
        return self.get(ids)

    def create(self, d):
        if "contact" not in d:
            raise Exception("contact key required by CPlus")
        if "contactId" in d["contact"]:
            del d["contact"]["contactId"]
        response = requests.post(
            url=CPLUS_CREATE_CONTACTS_URL,
            headers=self._get_header(),
            data=json.dumps(d)
        )
        if not response.ok:
            raise Exception(
                f"Error: code {response.status_code}, text: {response.text},"
                f" could not create contact in cplus {d}"
            )

    def delete(self, c):
        # need to make sure we have most up to date etag
        c_to_delete = self.get(c.cplusid)[0]
        d = {"contactId": c.cplusid, "etag": c_to_delete._etag}
        response = requests.post(
            url=CPLUS_DELETE_CONTACTS_URL,
            headers=self._get_header(),
            data=json.dumps(d)
        )
        if not response.ok:
            raise Exception(
                f"Error: code {response.status_code}, text: {response.text}, "
                f"could not delete contact from cplus "
                f"{c.fn} {c.ln} {c.cplusid}"
            )

    def update(self, c):
        cd = CPlusContact.to_api(c, include_etag=True)
        response = requests.post(
            url=CPLUS_UPDATE_CONTACTS_URL,
            headers=self._get_header(),
            data=json.dumps(cd)
        )
        if not response.ok:
            raise Exception(
                f"Error: code {response.status_code}, text: {response.text},"
                f" could not update contact {cd}"
            )

    def list(self, size=1000):
        got = -1
        from_cplus = []
        # using the scroll API gets you a subset of fields, unfortunately so we
        # need to query each one
        cursor = None
        while(got < 0 or got == size):
            params = {"size": size, "includeDeletedContacts": False}
            if cursor is not None:
                params['scrollCursor'] = cursor
            response = requests.post(
                url=CPLUS_SCROLL_CONTACTS_URL,
                headers=self._get_header(),
                data=json.dumps(params)
            )
            output_d = response.json()
            got = len(output_d["contacts"])
            from_cplus.extend(output_d["contacts"])
            cursor = output_d["cursor"]
        # remove dups
        idlist = list(set([cd["contactId"] for cd in from_cplus]))
        output = []
        # get can only take 100 max
        for chunk in _chunks(idlist,100):
            output.extend(self.get(chunk))
        return output

    def query(self, query_dict):
        response = requests.post(
            url=CPLUS_SEARCH_CONTACTS_URL,
            headers=self._get_header(),
            data=json.dumps(query_dict)
        )
        if not response.ok:
            raise Exception(
                f"Error: code {response.status_code}, text: {response.text}"
                f" could not get cplus contacts by query ({query_dict})"
            )
        return self._convert_to_contact_and_drop_none(response.json())

    def create_batch(self, batch, error_on_fail=False):
        errors = []
        for cd in batch:
            try:
                self.create(cd)
            except Exception as e:
                if error_on_fail:
                    raise
                errors.append(e)
        return errors

    def update_batch(self, batch, error_on_fail=False):
        errors = []
        for c in batch:
            try:
                self.update(c)
            except Exception as e:
                if error_on_fail:
                    raise
                errors.append(e)
        return errors

class CPlusAddress(Address):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_api(cls, cplus, ctype=None, **kwargs):
        iprefix = Address._get_type_prefix(ctype)
        item = CPlusAddress()
        addresses = {x["type"]: x for x in cplus.get('addresses', {})}
        addr = addresses.get(iprefix, {})
        streetaddr = _rowget(addr, "street")
        if streetaddr is not None:
            streetaddrs = streetaddr.split("\n")
            item.addr1 = streetaddrs[0]
            if len(streetaddrs) > 1:
                item.addr2 = streetaddrs[1]

        addr2 = _rowget(addr, "extendedAddress", "")
        if addr2 is not None:
            if item.addr2 is not None:
                item.addr2 += addr2
            else:
                item.addr2 = addr2
        item.city = _rowget(addr, "city")
        item.region = _rowget(addr, "region")
        item.zip = _rowget(addr, "postalCode")
        item.country = _rowget(addr, "country")
        item._type = ctype
        item.adjust_zip()
        item.adjust_country()
        return item

    @classmethod
    def to_api(cls, addr, **kwargs):
        d = {}
        if addr is None or addr.countfields() == 0:
            return d
        d["type"] = Address._get_type_prefix(addr._type)
        d["street"] = _str_not_none(getattr(addr, "addr1", ""))
        d["extendedAddress"] = _str_not_none(getattr(addr, "addr2", ""))
        d["city"] = _str_not_none(getattr(addr, "city", ""))
        d["region"] = _str_not_none(getattr(addr, "region", ""))
        d["postalCode"] = _str_not_none(getattr(addr, "zip", ""))
        d["country"] = _str_not_none(getattr(addr, "country", ""))
        return d


class CPlusContact(Contact):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def ids(cls):
        return [ "cplusid" ]

    @classmethod
    def from_api(cls, datarow, **kwargs):
        import itertools

        c = CPlusContact()
        c._id = datarow['contactId']
        c.cplusid = c._id
        c._fs = "CPlus"
        c._etag = datarow["etag"]
        cplus = datarow['contactData']

        c.waddr = CPlusAddress.from_api(cplus, ctype=ContactType.Work)
        c.haddr = CPlusAddress.from_api(cplus, ctype=ContactType.Home)
        c.h2addr = CPlusAddress.from_api(cplus, ctype=ContactType.Home2)

        c.notes = _rowget(cplus, "notes")
        if c.notes is not None and c.notes.find("Display Name:") > 0:
            c.notes = ""

        name = cplus.get('name', {})
        if len(name) == 0:
            return c

        c.fn = _rowget(name, 'givenName')
        c.ln = _rowget(name, 'familyName')
        c.mn = _rowget(name, 'middleName')

        if ((c.ln is None or not len(c.ln))
                and (c.fn is None or not len(c.fn))):
            return None

        c.prefix = _rowget(name, "prefix")
        c.suffix = _rowget(name, 'suffix')

        emails = _make_dict_from_list(cplus.get('emails', {}))
        c.email1 = _rowget(emails, "Home")
        c.email2 = _rowget(emails, "Work")
        c.authemail = _rowget(emails, "Authorized")

        emails = cplus.get("emails", [])
        if len(emails):
            if c.email1 is None:
                c.email1 = emails[0]["value"]
            if len(emails) > 1 and c.email2 is None:
                c.email2 = emails[1]["value"]

        phones = _make_dict_from_list(cplus.get('phoneNumbers', {}))
        c.mobilephone = Phone.make(
            _rowget(phones, 'Mobile'), PhoneType.Mobile).stringify()
        c.mobile2phone = Phone.make(
            _rowget(phones, 'Mobile2'), PhoneType.Mobile2).stringify()
        c.mobile3phone = Phone.make(
            _rowget(phones, 'Mobile3'), PhoneType.Mobile3).stringify()
        c.otherphone = Phone.make(
            _rowget(phones, 'Other'), PhoneType.Other).stringify()
        c.other2phone = Phone.make(
            _rowget(phones, 'Other2'), PhoneType.Other2).stringify()
        c.homephone = Phone.make(
            _rowget(phones, 'Home'), PhoneType.Home).stringify()
        c.workphone = Phone.make(
            _rowget(phones, 'Work'), PhoneType.Work).stringify()
        c.home2phone = Phone.make(
            _rowget(phones, 'Home2'), PhoneType.Home2).stringify()
        c.work2phone = Phone.make(
            _rowget(phones, 'Work2'), PhoneType.Work2).stringify()
        c.mainphone = Phone.make(
            _rowget(phones, 'Main'), PhoneType.Work).stringify()
        c.asstphone = Phone.make(
            _rowget(phones, 'Assistant'), PhoneType.Asst).stringify()

        c.url = ""
        urls = cplus.get("urls", [])
        if len(urls):
            c.url = _rowget(urls[0], "value")

        urls = _make_dict_from_list(cplus.get("urls",[]))
        c.linkedin = _rowget(urls, "linkedin")

        photos = cplus.get("photos",[])
        if len(photos):
            c.photo = _rowget(photos[0], "value")

        orgs = cplus.get("organizations", [])
        org = {}
        if len(orgs):
            org = orgs[0]
        c.org = _rowget(org, "description")
        c.jobtitle = _rowget(org, "title")
        c.company = _rowget(org, "name")

        items = cplus.get("relatedPeople", [])
        items.extend(cplus.get("items", []))
        items = _make_dict_from_list(items)
        c.nn = _rowget(items, 'Nickname')
        c.title = _rowget(items, "Title")
        c.social = _rowget(items, "Social")
        c.uid = _rowget(items, "UniqueID")
        c.atid = _rowget(items, "AirtableID")
        c.gid = _rowget(items, "OldGoogleID")
        c.gcid = _rowget(items, "GoogleContactID")
        c.altgcid = _rowget(items, "AltGoogleContactID")
        c.customterm = _rowget(items, "Custom Additional Mailing Term")
        c.customrepl = _rowget(items, "Custom Replacement Mailing Term")
        c.source = _rowget(items, "Source")
        c.spouseid = _rowget(items, "SpouseID")
        c.category = [x for x in _rowget(
            items, "Category", "").split(";") if x]
        c.holidaylists = [x for x in _rowget(
            items, "HolidayLists", "").split(";") if x]
        c.isholiday = _rowget(items, "IsHoliday", None, bool)
        c.isandfamily = _rowget(items, "Use And Family Syntax", None, bool)
        c.isworkmain = _rowget(items, "Use Work Address As Main", None, bool)
        c.isspouse = _rowget(items, "Treat As Spouse (default no)", None, bool)
        c.iscombosurname = _rowget(
            items, "Use Combination Surname for Family (default no)", None, bool)
        c.isspousemain = _rowget(
            items, "Use Spouse As Main Surname (default no)", None, bool)
        c.created = _rowget(items, "Created")
        c.lmod = _rowget(items, "LastModified")
        c.child1 = _rowget(items, "Child 1")
        c.child2 = _rowget(items, "Child 2")
        c.child3 = _rowget(items, "Child 3")
        c.child4 = _rowget(items, "Child 4")
        c.spouse = _rowget(items, 'Spouse')
        c.ltmod = None
        return c

    @classmethod
    def to_api(cls, c, include_etag=False, **kwargs):
        contact_dict = {}
        d = {}
        contact_dict["contact"] = {"contactId": getattr(c, "cplusid", None), "contactData": d}
        if include_etag:
            contact_dict["contact"]["etag"] = c._etag
        addresses = []
        for addr in ["haddr", "h2addr", "waddr"]:
            addr_dict = CPlusAddress.to_api(getattr(c, addr))
            if len(addr_dict):
                addresses.append(addr_dict)
        if len(addresses):
            d["addresses"] = addresses

        if c.birthday is not None:
            d["birthday"] = _str_not_none(c.birthday)
        anniv = c.anniversary
        if anniv is not None:
            y, m, d = _date_to_ymd(c.anniversary)
            d["dates"] = (
                [{
                    "type": "Anniversary",
                    "year": y, "month": m, "day": d
                  }
                 ]
            )
        emails = []
        if c.email1 is not None:
            emails.append({"type": "Home", "value": c.email1})
        if c.email2 is not None:
            emails.append({"type": "Work", "value": c.email2})
        if c.authemail is not None:
            emails.append({"type": "Authorized", "value": c.authemail})
        if len(emails):
            d["emails"] = emails

        phones = []
        if c.mobilephone is not None and len(c.mobilephone):
            phones.append({"type": "Mobile", "value": c.mobilephone})
        if c.mobile2phone is not None and len(c.mobile2phone):
            phones.append({"type": "Mobile2", "value": c.mobile2phone})
        if c.mobile3phone is not None and len(c.mobile3phone):
            phones.append({"type": "Mobile3", "value": c.mobile3phone})
        if c.otherphone is not None and len(c.otherphone):
            phones.append({"type": "Other", "value": c.otherphone})
        if c.other2phone is not None and len(c.other2phone):
            phones.append({"type": "Other2", "value": c.other2phone})
        if c.homephone is not None and len(c.homephone):
            phones.append({"type": "Home", "value": c.homephone})
        if c.home2phone is not None and len(c.home2phone):
            phones.append({"type": "Home2", "value": c.home2phone})
        if c.workphone is not None and len(c.workphone):
            phones.append({"type": "Work", "value": c.workphone})
        if c.work2phone is not None and len(c.work2phone):
            phones.append({"type": "Work2", "value": c.work2phone})
        if c.asstphone is not None and len(c.asstphone):
            phones.append({"type": "Assistant", "value": c.asstphone})
        if c.mainphone is not None and len(c.mainphone):
            phones.append({"type": "Main", "value": c.mainphone})
        if len(phones):
            d["phoneNumbers"] = phones

        d["name"] = {"givenName": c.fn, "familyName": c.ln}
        if c.mn is not None and len(c.mn) > 0:
            d["name"]["middleName"] = c.mn
        elif c.mn is not None:
            d["name"]["middleName"] = None
        if c.prefix is not None:
            d["name"]["prefix"] = c.prefix
        if c.suffix is not None:
            d["name"]["suffix"] = c.suffix

        related = []
        if c.spouse is not None:
            related.append({"type": "Spouse", "value": c.spouse})
        if c.child1 is not None:
            related.append({"Type": "Child 1", "value": c.child1})
        if c.child2 is not None:
            related.append({"type": "Child 2", "value": c.child2})
        if c.child3 is not None:
            related.append({"type": "Child 3", "value": c.child3})
        if c.child4 is not None:
            related.append({"type": "Child 4", "value": c.child4})

        urls = []
        if c.url is not None:
            urls.append({"type": "", "value": c.url})

        if c.linkedin is not None:
            username = ""
            names = c.linkedin.split("/")
            if names:
                username = names[-1]
            urls.append({"type": "linkedin", "username": username, "value": c.linkedin })
        if len(urls):
            d["urls"] = urls

        if c.photo is not None:
            d["photos"] = [{"value": c.photo}]

        org = {}
        if c.org is not None:
            org["description"] = c.org
        if c.jobtitle is not None:
            org["title"] = c.jobtitle
        if c.company is not None:
            org["name"] = c.company
        if len(org):
            d["organizations"] = [org]

        if c.notes is not None:
            d["notes"] = c.notes

        # weird, but the CPlus API seems to ignore "items", but we can
        # store k/v in "relatedPeople"
        items = related
        if c.nn is not None:
            items.append({"type": "Nickname", "value": c.nn})
        if c.title is not None:
            items.append({"type": "Title", "value": c.title})
        if c.social is not None:
            items.append({"type": "Social", "value": c.social})
        if c.uid is not None:
            items.append({"type": "UniqueID", "value": str(c.uid)})
        if c.cplusid is not None:
            items.append({"type": "CPlusID", "value": c.cplusid})
        if c.atid is not None:
            items.append({"type": "AirtableID", "value": c.atid})
        if c.gid is not None:
            items.append({"type": "OldGoogleID", "value": c.gid})
        if c.gcid is not None:
            items.append({"type": "GoogleContactID", "value": c.gcid})
        if c.altgcid is not None:
            items.append({"type": "AltGoogleContactID", "value": c.altgcid})
        if c.customterm is not None:
            items.append(
                {"type": "Custom Additional Mailing Term", "value": c.customterm})
        if c.customrepl is not None:
            items.append(
                {"type": "Custom Replacement Mailing Term", "value": c.customrepl})
        if c.source is not None:
            items.append({"type": "Source", "value": c.source})
        if c.spouseid is not None:
            items.append({"type": "SpouseID", "value": c.spouseid})
        if c.category is not None and len(c.category):
            items.append({"type": "Category", "value": ";".join(c.category)})
        if c.holidaylists is not None and len(c.holidaylists):
            items.append(
                {"type": "HolidayLists", "value": ";".join(c.holidaylists)})
        if c.isholiday is not None:
            items.append({"type": "IsHoliday", "value": str(c.isholiday)})
        if c.isandfamily is not None:
            items.append(
                {"type": "Use And Family Syntax", "value": str(c.isandfamily)})
        if c.isworkmain is not None:
            items.append(
                {"type": "Use Work Address As Main", "value": str(c.isworkmain)})
        if c.isspouse is not None:
            items.append(
                {"type": "Treat As Spouse (default no)", "value": str(c.isspouse)})
        if c.iscombosurname is not None:
            items.append(
                {"type": "Use Combination Surname for Family (default no)", "value": str(c.iscombosurname)})
        if c.isspousemain is not None:
            items.append(
                {"type": "Use Spouse As Main Surname (default no)", "value": str(c.isspousemain)})
        if c.created is not None:
            items.append({"type": "Created", "value": c.created})
        if c.lmod is not None:
            items.append({"type": "LastModified", "value": c.lmod})

        if len(related):
            d["relatedPeople"] = related

        return contact_dict
