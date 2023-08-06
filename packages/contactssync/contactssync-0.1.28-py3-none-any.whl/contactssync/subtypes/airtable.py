import attr
from airtable import Airtable
import collections
import datetime
import dateutil
import functools

from ..base import Contact
from ..addresses import Address
from ..types import OptStr, PhoneType, ContactType
from ..utils import (
    _rowget,
    _tolower,
    _str_not_none,
    _date_to_ymd,
    _make_dict_from_list,
    _chunks,
    _strip_bad_chars,
)
from ..phones import Phone
from ..connect import Connection

@attr.s(auto_attribs=True)
class AirtableConnection(Connection):
    base_name: str
    table_name: str
    api_key: str

    def __attrs_post_init__(self):
        self._atb = Airtable(self.base_name, self.table_name, self.api_key)

    @classmethod
    def contact_type(cls):
        return AirtableContact

    @classmethod
    def dict_to_contact(cls, d, **kwargs):
        return AirtableContact.from_api(d, **kwargs)

    @classmethod
    def contact_to_dict(cls, c, **kwargs):
        return AirtableContact.to_api(c, **kwargs)

    def get(self, id, convert=True):
        if convert:
            return self._convert_to_contact_and_drop_none(self._atb.get(id))[0]
        return self._atb.get(id)

    @classmethod
    def build_query_formula(cls, fields, and_or="AND"):
        query_string = and_or + "("
        first = True
        for f, v in fields.items():
            if not first:
                query_string += ","
            first = False
            query_string += f"(FIND('{v}', {{{f}}})=1)"
        query_string += ")"
        return query_string

    def query(self, query_dict, convert=True):
        vals = self._atb.get_all(formula=self.build_query_formula(query_dict))
        if convert:
            return self._convert_to_contact_and_drop_none(vals)
        return vals

    def get_by_name(self, fn, ln, convert=True):
        return self.query({"First Name": fn, "Last Name": ln}, convert=convert)

    def create(self, d):
        if "fields" not in d:
            raise Exception("must provide 'fields'")
        return self._atb.insert(d["fields"], typecast=True)["id"]

    def delete(self, c):
        self._atb.delete(c.atid)

    def _get_updated_fields(self, c):
        curcd = self.contact_to_dict(self.get(c.atid))
        curcf = {
            f: v for f, v in curcd["fields"].items() if (
                    f not in [ "Last Modified", "Created", "ID", "AirtableID" ] and
                    "AUTOMATED" not in f
                )
        }
        cd = self.contact_to_dict(c)
        cdf = cd["fields"]
        outfields = {}
        outfields = {}
        for field,value in cdf.items():
            if ( (field not in curcf or curcf[field] != cdf[field]) and
                 cdf[field] is not None and
                 (isinstance(cdf[field], bool) or len(cdf[field]))):
                outfields[field] = value
        return outfields

    def update(self, c):
        outfields = self._get_updated_fields(c)
        self._atb.update(c.atid, outfields)

    def list(self):
        return self._convert_to_contact_and_drop_none(
            self._atb.get_all()
        )

    def create_batch(self, batch):
        dbatch = []
        for cf in batch:
            if cf is not None and len(cf) > 0:
                dbatch.append(cf["fields"])
        if len(dbatch) == 0:
            return

        for subdbatch in _chunks(dbatch, 10):
            records = self._atb.batch_insert(subdbatch, typecast=True)
        if records is None or len(records) == 0:
            return []
        return [ r["id"] for r in records ]

    def update_batch(self, batch):
        dbatch = []
        for c in batch:
            outfields = self._get_updated_fields(c)
            update = { "fields": outfields, "id": c.atid }
            dbatch.append(update)

        if len(dbatch) == 0:
            return

        for subdbatch in _chunks(dbatch, 10):
            self._atb.batch_update(subdbatch, typecast=True)

class AirtableAddress(Address):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_api(cls, row, ctype=None, **kwargs):
        iprefix = Address._get_type_prefix(ctype)
        item = Address()

        streetaddr = _strip_bad_chars(_rowget(row,f"{iprefix} Street Address"))
        if streetaddr is not None:
            streetaddrs = streetaddr.split("\n")
            item.addr1 = streetaddrs[0]
            if len(streetaddrs) > 1:
                item.addr2 = streetaddrs[1]

        addr2 = _strip_bad_chars(_rowget(row,f"{iprefix} Street Address 2"))
        if addr2 is not None:
            if item.addr2 is not None:
                item.addr2 += addr2
            else:
                item.addr2 = addr2
        item.city  = _strip_bad_chars(_rowget(row,f"{iprefix} City"))
        item.region = _strip_bad_chars(_rowget(row,f"{iprefix} State"))
        item.country = _strip_bad_chars(_rowget(row,f"{iprefix} Country/Region"))
        item.zip = _strip_bad_chars(_rowget(row,f"{iprefix} Zip"))
        item._type = ctype
        item.adjust_zip()
        item.adjust_country()
        return item

    @classmethod
    def to_api(cls, addr, **kwargs):
        d = {}
        if addr is None or addr.countfields() == 0:
            return d
        prefix = Address._get_type_prefix(addr._type)
        d[f"{prefix} Street Address"] = _strip_bad_chars(_str_not_none(getattr(addr, "addr1", "")))
        d[f"{prefix} Street Address 2"] = _strip_bad_chars(_str_not_none(getattr(addr, "addr2", "")))
        d[f"{prefix} City"] = _strip_bad_chars(_str_not_none(getattr(addr, "city", "")))
        d[f"{prefix} State"] = _strip_bad_chars(_str_not_none(getattr(addr, "region", "")))
        d[f"{prefix} Zip"] = _strip_bad_chars(_str_not_none(getattr(addr, "zip", "")))
        d[f"{prefix} Country/Region"] = _strip_bad_chars(_str_not_none(getattr(addr, "country", "")))
        return d

class AirtableContact(Contact):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def ids(cls):
        return ["atid"]


    @classmethod
    @functools.lru_cache(100)
    def is_primary(cls, fld):
        if fld.lower() in cls.ids():
            return True
        if fld.lower().startswith("is"):
            return True
        if "holiday" in fld.lower():
            return True
        if fld.lower() in [ "lmod", "created", "uid" ]:
            return True
        # temporary
        if fld.lower() == "cplusid":
            return True
        return False

    @classmethod
    def multi_to_list(cls, s):
        if isinstance(s, list):
            return s
        if isinstance(s, str):
            return [ subs.strip() for subs in s.split(";") ]
        raise Exception(f"Invalid input {s}, not list or string")

    @classmethod
    def to_api(cls, c, **kwargs):
        record = {}
        d = {}
        record["id"] = c.atid
        record["fields"] = d

        for addr in [ "haddr", "h2addr", "waddr" ]:
            addr_dict = AirtableAddress.to_api(getattr(c, addr))
            if len(addr_dict):
                d.update(addr_dict)

        if c.birthday is not None:
            d["Birthday"] = c.birthday
        if c.anniversary is not None:
            d["Anniversary"] = c.anniversary

        if c.email1 is not None:
            d["Email Address 1"] = _strip_bad_chars(c.email1)
        if c.email2 is not None:
            d["Email Address 2"] = _strip_bad_chars(c.email2)
        if c.authemail is not None:
            d["Authorized Email"] = _strip_bad_chars(c.authemail)

        if c.mobilephone is not None and len(c.mobilephone):
            d["Mobile Phone"] = _strip_bad_chars(c.mobilephone)
        if c.mobile2phone is not None and len(c.mobile2phone):
            d["Mobile 2 Phone"] = _strip_bad_chars(c.mobile2phone)
        if c.mobile3phone is not None and len(c.mobile3phone):
            d["Mobile 3 Phone"] = _strip_bad_chars(c.mobile3phone)
        if c.otherphone is not None and len(c.otherphone):
            d["Other Phone"] = _strip_bad_chars(c.otherphone)
        if c.other2phone is not None and len(c.other2phone):
            d["Other 2 Phone"] = _strip_bad_chars(c.other2phone)
        if c.homephone is not None and len(c.homephone):
            d["Home Phone"] = _strip_bad_chars(c.homephone)
        if c.home2phone is not None and len(c.home2phone):
            d["Home 2 Phone"] = _strip_bad_chars(c.home2phone)
        if c.workphone is not None and len(c.workphone):
            d["Work Phone"] = _strip_bad_chars(c.workphone)
        if c.work2phone is not None and len(c.work2phone):
            d["Work 2 Phone"] = _strip_bad_chars(c.work2phone)
        if c.asstphone is not None and len(c.asstphone):
            d["Assistant Phone"] = _strip_bad_chars(c.asstphone)
        if c.mainphone is not None and len(c.mainphone):
            d["Main Phone"] = _strip_bad_chars(c.mainphone)
        if c.workfax is not None and len(c.workfax):
            d["Work Fax"] = _strip_bad_chars(c.workfax)

        if c.fn is not None:
            d["First Name"] = c.fn
        if c.ln is not None:
            d["Last Name"] = c.ln
        if c.mn is not None:
            d["Middle Name"] = c.mn
        if c.nn is not None:
            d["Nickname"] = c.nn

        if c.prefix is not None:
            d["Prefix"] = _strip_bad_chars(c.prefix)
        if c.suffix is not None:
            d["Suffix"] = _strip_bad_chars(c.suffix)
        if c.title is not None:
            d["Title"] = _strip_bad_chars(c.title)

        if c.spouse is not None:
            d["Spouse"] = _strip_bad_chars(c.spouse)
        if c.child1 is not None:
            d["Child 1"] = _strip_bad_chars(c.child1)
        if c.child2 is not None:
            d["Child 2"] = _strip_bad_chars(c.child2)
        if c.child3 is not None:
            d["Child 3"] = _strip_bad_chars(c.child3)
        if c.child4 is not None:
            d["Child 4"] = _strip_bad_chars(c.child4)

        if c.url is not None:
            d["URL"] = c.url

        if c.org is not None:
            d["Organization"] = _strip_bad_chars(c.org)
        if c.jobtitle is not None:
            d["Job Title"] = _strip_bad_chars(c.jobtitle)
        if c.company is not None:
            d["Company"] = _strip_bad_chars(c.company)
        if c.notes is not None:
            d["Notes"] = c.notes
        if c.social is not None:
            d["Social"] = c.social
        if c.cplusid is not None:
            d["ContactPlusID"] = c.cplusid
        if c.gid is not None:
            d["OldGoogleID"] = c.gid
        if c.gcid is not None:
            d["GoogleContactID"] = c.gcid
        if c.altgcid is not None:
            d["AltGoogleContactID"] = c.altgcid
        if c.customterm is not None:
            d["Custom Additional Mailing Term"] = c.customterm
        if c.customrepl is not None:
            d["Custom Replacement Mailing Term"] = c.customrepl
        if c.source is not None:
            d["Source"] = c.source
        if c.spouseid is not None:
            d["SpouseID"] = c.spouseid
        if c.category is not None and len(c.category):
            d["Category"] = AirtableContact.multi_to_list(c.category)
        if c.holidaylists is not None and len(c.holidaylists):
            d["HolidayLists"] = AirtableContact.multi_to_list(c.holidaylists)
        if c.isholiday is not None:
            d["IsHoliday"] = c.isholiday
        if c.isandfamily is not None:
            d["Use And Family Syntax"] = c.isandfamily
        if c.isworkmain is not None:
            d["Use Work Address As Main"] = c.isworkmain
        if c.isspouse is not None:
            d["Treat As Spouse (default yes)"] = c.isspouse
        if c.iscombosurname is not None:
            d["Use Combination Surname For Family (default no)"] = c.iscombosurname
        if c.isspousemain is not None:
            d["Use Spouse as Main Surname (default no)"] = c.isspousemain
        if c.linkedin is not None:
            d["LinkedIn"] = c.linkedin
        if c.photo is not None:
            d["Photo"] = c.photo
        return record

    @classmethod
    def from_api(cls, datarow, **kwargs):
        c = AirtableContact()
        c._fs = "Airtable"
        c._id = datarow['id']
        row = datarow['fields']
        c.ln = _rowget(row, 'Last Name')
        if c.ln is not None:
            c.ln = c.ln.strip()
        c.fn = _rowget(row,'First Name')
        if c.fn is not None:
            c.fn = c.fn.strip()

        if ( (c.ln is None or not len(c.ln) ) and
             (c.fn is None or not len(c.fn) ) ):
             return None

        c.waddr = AirtableAddress.from_api(row, ctype=ContactType.Work)
        c.haddr = AirtableAddress.from_api(row, ctype=ContactType.Home)
        c.h2addr = AirtableAddress.from_api(row, ctype=ContactType.Home2)
        if c.h2addr == c.haddr:
            c.h2addr = AirtableAddress()

        c.mn = _rowget(row, 'Middle Name')
        if c.mn is not None:
            c.mn = c.mn.strip()
        c.nn = _rowget(row, 'Nickname')
        if c.nn is not None:
            c.nn = c.nn.strip()
        c.url = _rowget(row, "URL")
        c.title = _rowget(row, 'Title')
        c.prefix = _rowget(row, "Prefix")
        c.suffix = _rowget(row, 'Suffix')
        c.category = _rowget(row, 'Category', [])
        c.source = _rowget(row, 'Source')
        c.email1 = _rowget(row, 'Email Address 1')
        c.email2 = _rowget(row, 'Email Address 2')
        if c.email1 == c.email2:
            #c.email2 = None
            pass

        c.authemail = _rowget(row, 'Authorized Email')
        c.mainphone = Phone.make(_rowget(row, 'Main Phone'), PhoneType.Main).stringify()
        c.homephone = Phone.make(_rowget(row, 'Home Phone'), PhoneType.Home).stringify()
        c.workphone = Phone.make(_rowget(row, 'Work Phone'), PhoneType.Work).stringify()
        c.home2phone = Phone.make(_rowget(row, 'Home 2 Phone'), PhoneType.Home2).stringify()
        c.work2phone = Phone.make(_rowget(row, 'Work 2 Phone'), PhoneType.Work2).stringify()

        if c.homephone == c.home2phone:
            pass
            #c.home2phone = None
        if c.workphone == c.work2phone:
            pass
            #c.work2phone = None

        c.asstphone = Phone.make(_rowget(row, 'Assistant Phone'), PhoneType.Asst).stringify()
        c.mobilephone = Phone.make(_rowget(row, 'Mobile Phone'), PhoneType.Mobile).stringify()
        c.mobile2phone = Phone.make(_rowget(row, 'Mobile 2 Phone'), PhoneType.Mobile2).stringify()
        c.mobile3phone = Phone.make(_rowget(row, 'Mobile 3 Phone'), PhoneType.Mobile3).stringify()
        if c.mobilephone == c.mobile2phone:
            pass
            #c.mobile2phone = None
        if c.mobilephone == c.mobile3phone:
            pass
            #c.mobile3phone = None
        if c.mobile2phone == c.mobile3phone:
            pass
            #c.mobile3phone = None

        c.otherphone = Phone.make(_rowget(row, 'Other Phone'), PhoneType.Other).stringify()
        c.other2phone = Phone.make(_rowget(row, 'Other 2 Phone'), PhoneType.Other2).stringify()
        if c.otherphone == c.other2phone:
            c.other2phone = None

        c.photo = _rowget(row, "Photo")
        c.linkedin = _rowget(row, "LinkedIn")
        c.social = _rowget(row, 'Social')
        c.uid = str(_rowget(row, 'UniqueID'))
        c.cplusid = _rowget(row, "ContactPlusID")
        c.atid = c._id
        c.child1 = _rowget(row, "Child 1")
        c.child2 = _rowget(row, "Child 2")
        c.child3 = _rowget(row, "Child 3")
        c.child4 = _rowget(row, "Child 4")
        c.spouse = _rowget(row, 'Spouse')
        c.spouseid = _rowget(row, 'SpouseID')
        c.org = _rowget(row, "Organization")
        c.company = _rowget(row, "Company")
        c.jobtitle = _rowget(row, "Job Title")
        c.notes = _rowget(row, "Notes")
        c.anniversary = _rowget(row, "Anniversary")
        c.birthday = _rowget(row, "Birthday")
        c.customterm = _rowget(row, "Custom Additional Mailng Term")
        c.customrepl = _rowget(row, "Custom Replacement Mailing Term")
        c.atid = _rowget(row, "AirtableID")
        c.gid = _rowget(row, "OldGoogleID")
        c.gcid = _rowget(row, "GoogleContactID")
        c.altgcid = _rowget(row, "AltGoogleContactID")
        c.holidaylists = _rowget(row, "HolidayLists", [])
        c.isholiday = _rowget(row, "IsHoliday", None, bool)
        c.isandfamily = _rowget(row, "Use And Family Syntax", None, bool)
        c.isworkmain = _rowget(row, "Use Work Address As Main", None, bool)
        c.isspouse = _rowget(row, "Treat As Spouse (default no)", None, bool)
        c.iscombosurname = _rowget(row, "Use Combination Surname For Family (default no)", None, bool)
        c.isspousemain = _rowget(row, "Use Spouse As Main Surname (default no)", None, bool)
        c.created = _rowget(row, "Created")
        c.lmod = _rowget(row, "Last Modified")
        try:
            c.lmoddt = dateutil.parser.isoparse(c.lmod)
        except ValueError:
            c.lmoddt = None
        if c.created is None:
            c.createddt = datetime.datetime(datetime.MAXYEAR, 1, 1,0,0,0, tzinfo=datetime.timezone.utc)
            c.createddt = dateutil.parser.isoparse(c.created)
        return c
