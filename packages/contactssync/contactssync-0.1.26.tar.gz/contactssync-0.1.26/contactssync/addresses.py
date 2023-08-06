
from abc import abstractclassmethod
import attr
import datetime
import pandas as pd
import re

from .types import OptStr, ContactType, Comparison
from .utils import _rowget, _tolower, _str_not_none, _strip_bad_chars

@attr.s(auto_attribs=True)
class Address:
    _type: ContactType = attr.ib(eq=False, default=ContactType.Unknown)
    addr1: OptStr = attr.ib(eq=_tolower, default=None, converter=_strip_bad_chars)
    addr2: OptStr = attr.ib(eq=_tolower, default=None, converter=_strip_bad_chars)
    city: OptStr = attr.ib(eq=_tolower, default=None, converter=_strip_bad_chars)
    region: OptStr = attr.ib(eq=_tolower, default=None, converter=_strip_bad_chars)
    zip: OptStr = attr.ib(eq=_tolower, default=None, converter=_strip_bad_chars)
    country: OptStr = attr.ib(eq=_tolower, default=None, converter=_strip_bad_chars)

    def to_series(self):
        t = self._type.value.lower()
        return pd.Series({
            f"{t}_addr1": self.addr1,
            f"{t}_addr2": self.addr2,
            f"{t}_city": self.city,
            f"{t}_region": self.region,
            f"{t}_zip": self.zip,
            f"{t}_country": self.country,
        })

    def countfields(self):
        num = 0
        for fld in attr.fields(Address):
            if fld.name == "type" or fld.name == "_type":
                continue
            attrval = getattr(self, fld.name, None)
            if attrval is not None and len(attrval.strip()):
                num += 1
        return num

    def adjust_country(self):
        if _tolower(self.country) in ['us','usa','united states','america','united states of america']:
            self.country = 'us'

    def adjust_zip(self):
        if _tolower(self.country) in ['us','usa','united states','america','united states of america']:
            return Address.adjust_zip_us(self.zip)

    @staticmethod
    def adjust_zip_us(zip):
        if zip is not None and len(zip) < 5:
            zip = "%05s" % zip
        return zip

    @staticmethod
    def _get_type_prefix(ctype):
        iprefix = None
        match = re.match("^([A-Za-z]+)(\d*)$", ctype.value)
        if match:
            iprefix = (f"{match.group(1)} {match.group(2)}").strip()
        else:
            raise Exception(f"Invalid address type ({ctype}) provided")
        return iprefix

    @abstractclassmethod
    def from_api(cls, row, **kwargs):
        raise NotImplementedError()

    @abstractclassmethod
    def to_api(cls, addr, **kwargs):
        raise NotImplementedError()

    def compare(self, other):
        selfcount = 0
        if self is not None:
            selfcount = self.countfields()
        othercount = 0
        if other is not None:
            othercount = other.countfields()
        if selfcount == 0 and othercount == 0:
            return True, Comparison.BothInvalid
        if selfcount > othercount:
            return False, Comparison.Left
        elif selfcount < othercount:
            return False, Comparison.Right
        else:
            for fld in attr.fields(self.__class__):
                if "_" in fld.name:
                    continue
                if _tolower(getattr(self, fld.name)) != _tolower(getattr(other, fld.name)):
                    return False, Comparison.EqualOrUnclear
        return True, Comparison.EqualOrUnclear
