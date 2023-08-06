
import attr
import phonenumbers
from typing import Optional

from .types import OptPhone, PhoneType


@attr.s(auto_attribs=True)
class Phone:
    _type: PhoneType = PhoneType.Unknown
    number = OptPhone = None

    @classmethod
    def make(cls, pnstr, type=PhoneType.Unknown):
        if pnstr is None:
            pnstr = ""
        if not isinstance(pnstr, str) and not isinstance(pnstr, phonenumbers.PhoneNumber):
            raise Exception("invalid type provided to make")
        pn = Phone()
        pn._type = type
        try:
            pn.number = phonenumbers.parse(pnstr, None)
        except phonenumbers.NumberParseException:
            try:
                pn.number = phonenumbers.parse(pnstr, "US")
            except phonenumbers.NumberParseException:
                try:
                    pn.number = phonenumbers.parse(f"+{pnstr}", None)
                except phonenumbers.NumberParseException:
                    pass
        return pn

    def stringify(self):
        if self.number is None:
            return ""
        return phonenumbers.format_number(self.number, phonenumbers.PhoneNumberFormat.E164)
