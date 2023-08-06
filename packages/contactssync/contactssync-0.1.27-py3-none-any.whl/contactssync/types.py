
from enum import Enum, IntEnum
import phonenumbers
from typing import Optional

OptPhone = Optional[phonenumbers.PhoneNumber]
OptStr = Optional[str]

class ContactType(Enum):
    Home = "Home"
    Home2 = "Home2"
    Work = "Work"
    Work2 = "Work2"
    Other = "Other"
    Unknown = "Unknown"

class PhoneType(Enum):
    Home = "Home"
    Home2 = "Home2"
    Work = "Work"
    Work2 = "Work2"
    Mobile = "Mobile"
    Mobile2 = "Mobile2"
    Mobile3 = "Mobile3"
    Other = "Other"
    Other2 = "Other2"
    Main = "Main"
    Asst = "Asst"
    Unknown = "Unknown"

class Comparison(IntEnum):
    EqualOrUnclear = 0
    Left = -1
    Right = 1
    BothInvalid = -2
