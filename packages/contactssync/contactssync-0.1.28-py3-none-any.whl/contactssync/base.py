from enum import Enum, IntEnum
from abc import ABC, abstractclassmethod, abstractmethod
import attr
import collections
import datetime
import functools
import itertools
import pandas as pd
import re
from typing import Any, Dict, List, Optional

from .nicknames import get_nicknames
from .types import OptStr, PhoneType, ContactType, Comparison
from .utils import (
    _rowget,
    _both_none,
    _tolower,
    _str_not_none,
    _date_to_ymd,
    _make_dict_from_list
)
from .phones import Phone
from .addresses import Address


def _isnull(s):
    if (s is None or (isinstance(s, str) and len(s.strip()) == 0) or
        (isinstance(s, collections.Iterable) and len(s) == 0) or
        (not isinstance(s, collections.Iterable) and pd.isnull(s))):
        return True
    return False

@attr.s(auto_attribs=True, eq=False)
class Contact(ABC):
    _id: OptStr = attr.ib(
        default=None,
        metadata={"is_metadata": True}
    )
    _fs: OptStr = attr.ib(
        default=None,
        metadata={"is_metadata": True}
    )
    _etag: OptStr = attr.ib(
        default=None,
        metadata={"is_metadata": True}
    )
    _source_dict: Dict[str, Any] = attr.ib(
        default=None,
        metadata={"is_metadata": True}
    )
    fn: OptStr = None
    ln: OptStr = None
    mn: OptStr = None
    nn: OptStr = None
    title: OptStr = None
    prefix: OptStr = None
    suffix: OptStr = None
    haddr: Optional[Address] = None
    h2addr: Optional[Address] = None
    waddr: Optional[Address] = None
    category: Optional[List[str]] = None
    source: OptStr = None
    email1: OptStr = None
    email2: OptStr = None
    authemail: OptStr = None
    mainphone: OptStr = None
    homephone: OptStr = None
    home2phone: OptStr = None
    workphone: OptStr = None
    work2phone: OptStr = None
    workfax: OptStr = None
    asstphone: OptStr = None
    mobilephone: OptStr = None
    mobile2phone: OptStr = None
    mobile3phone: OptStr = None
    otherphone: OptStr = None
    other2phone: OptStr = None
    social: OptStr = None
    uid: OptStr = None
    atid: OptStr = None
    cplusid: OptStr = None
    child1: OptStr = None
    child2: OptStr = None
    child3: OptStr = None
    child4: OptStr = None
    spouse: OptStr = None
    spouseid: OptStr = None
    org: OptStr = None
    company: OptStr = None
    jobtitle: OptStr = None
    notes: OptStr = None
    anniversary: OptStr = None
    birthday: OptStr = None
    customterm: OptStr = None
    customrepl: OptStr = None
    url: OptStr = None
    gid: OptStr = None
    gcid: OptStr = None
    altgcid: OptStr = None
    holidaylists: Optional[List[str]] = None
    isholiday: Optional[bool] = None
    isandfamily: Optional[bool] = None
    isworkmain: Optional[bool] = None
    isspouse: Optional[bool] = None
    isspousesurname: Optional[bool] = None
    iscombosurname: Optional[bool] = None
    isspousemain: Optional[bool] = None
    linkedin: OptStr = None
    photo: OptStr = attr.ib(
        default=None,
        metadata={"is_metadata": True}
    )
    created: OptStr = attr.ib(
        default=None,
        metadata={"is_metadata": True}
    )
    lmod: OptStr = attr.ib(
        default=None,
        metadata={"is_metadata": True}
    )
    createddt: datetime.datetime = attr.ib(
        factory=functools.partial(datetime.datetime.fromtimestamp,0),
        metadata={"is_metadata": True}
    )
    lmoddt: datetime.datetime = attr.ib(
        factory=functools.partial(datetime.datetime.fromtimestamp,0),
        metadata={"is_metadata": True}
    )

    def __attrs_post_init__(self):
        if self.holidaylists is None:
            self.holidaylists = []

    @classmethod
    def is_primary(cls, fld):
        return False

    @abstractclassmethod
    def from_api(cls, row, **kwargs):
        raise NotImplementedError()

    @abstractclassmethod
    def to_api(cls, c, **kwargs):
        raise NotImplementedError()

    def _dedup_attrs(self, attr1, attr2, comparison_=str.__eq__):
        val1 = getattr(self, attr1, None)
        val2 = getattr(self, attr2, None)
        if _both_none(val1, val2):
            return

        if  val1 is not None and val2 is not None and comparison_(val1,val2):
            setattr(self, attr2, None)

    def dedup_emails(self):
        # pref email 1 > email 2 > authorized email1()
        emails = [
            fld.name for fld in attr.fields(self.__class__) if "email" in fld.name
        ]
        email_pairs = itertools.combinations(emails, r=2)
        for e1, e2 in email_pairs:
            self._dedup_attrs(e1, e2)

    def dedup_phones(self):
        phones = [
            fld.name for fld in attr.fields(self.__class__) if "phone" in fld.name
        ]
        phone_pairs = itertools.combinations(phones, r=2)
        for p1, p2 in phone_pairs:
            self._dedup_attrs(p1, p2)

    def dedup_addrs(self):
        addresses = [
            fld.name for fld in attr.fields(self.__class__) if "addr" in fld.name
        ]
        addresses = [ "haddr", "h2addr", "waddr" ]
        addr_pairs = itertools.combinations(addresses, r=2)
        for a1, a2 in addr_pairs:
            self._dedup_attrs(a1, a2, comparison_=(lambda x,y: Address.compare(x,y)[0]))


    def dedup(self):
        self.dedup_emails()
        self.dedup_phones()
        self.dedup_addrs()

    def to_series(self, ignore_null=False):
        d = {}
        appends = []
        for fld in attr.fields(self.__class__):
            attrval = getattr(self, fld.name)
            if _isnull(attrval):
                continue
            to_s = getattr(attrval, "to_series", None)
            if to_s is not None:
                appends.append(to_s())
            else:
                d[fld.name] = attrval
        s = pd.Series(d)
        for append in appends:
            s = s.append(append)
        return s

    @classmethod
    def _make_column_index(cls,index):
        final_index = []
        index = list(set(index))
        if len(index) == 0:
            return index
        if "ln" not in index:
            index.insert(0,"ln")
        if "fn" not in index:
            index.insert(0,"fn")
        for k in index:
            fld = getattr(attr.fields(cls),k,None)
            if fld is not None and getattr(fld,"metadata").get("is_metadata",False):
                continue
            final_index.append(k)
        return final_index

    @staticmethod
    def _is_addr_indexfield(fld):
        return "_" in fld

    @classmethod
    def compare_df(cls, c1, c2, include_all=False):
        s1 = c1.to_series()
        s2 = c2.to_series()
        s1 = s1.reindex(s1.index.union(s2.index))
        s2 = s2.reindex(s2.index.union(s1.index))
        if not s1.index.equals(s2.index):
            raise Exception(
                "cannot compare two objects with non-matching indices\n"
                f"obj1: {s1.index}"
                f"obj2: {s2.index}"
            )
        keys = s1.index
        if not include_all:
            keys = []
            compare, results, _ = c1.compare(c2)
            index = s1.index
            if compare:
                return pd.DataFrame()
            else:
                index = [
                    k for k in index if (
                        cls._is_addr_indexfield(k) or
                        (k in results and results[k] in [Comparison.Left,Comparison.Right])
                    )
                ]
            index = Contact._make_column_index(index)
            index = [ k for k in index if ( k in s1.index and k in s2.index ) ]
            if len(index) is None:
                return pd.DataFrame()
            for k in index:
                if _isnull(s1.loc[k]) and _isnull(s2.loc[k]):
                    continue
                keys.append(k)

        d = { k: [ s1.loc[k], s2.loc[k] ] for k in keys }
        return pd.DataFrame(d)

    @classmethod
    def compare_visual(cls, c1, c2, compare_all=False):
        df = cls.compare_df(c1, c2, include_all=compare_all)
        if len(df) == 0:
            return None
        fs1 = c1._fs
        fs2 = c2._fs
        if fs1 == fs2:
            fs1 = f"{fs1}_1"
            fs2 = f"{fs2}_2"
        tdf = df.T.rename(columns={0: fs1, 1: fs2})
        if compare_all:
            cell_color_series = [ str(
                all([x == y for x,y in zip(
                            df[k], df[k].reindex(index=df.index[::-1])
                        )
                    ])).lower() + " " for k in df.columns
            ]
            cell_color = pd.DataFrame(
                { ind:cell_color_series for ind in tdf.columns}, index=tdf.index
            )
        else:
            cell_color = pd.DataFrame(
                {k: [ "true" if k == fs1 else "false" for i in tdf.index] for k in tdf.columns },
                index=tdf.index, columns=tdf.columns
            )

        styler = tdf.style
        styler = styler.set_table_styles([  # create internal CSS classes
            {'selector': '.false', 'props':[("background-color", "#ffe6e6;")]},
            {'selector': '.true', 'props': [("background-color", "#8cf06a;")]},
        ], overwrite=False)
        styler = styler.set_td_classes(cell_color)
        return styler


    @property
    def id(self):
        return self._id

    @classmethod
    @abstractmethod
    def ids(cls):
        raise NotImplementedError("must implement 'ids'")

    @staticmethod
    def get_field_parts(fldname):
        match = re.match("^([a-z]+)(\d+)([a-z]*)$", fldname)
        if not match:
            return fldname, 1
        root = f"{match.group(1)}{match.group(3)}".strip()
        num = int(match.group(2))
        return root, num

    @staticmethod
    def _compare_attr(selfattr, otherattr, default_compare=Comparison.EqualOrUnclear):
        compval = None
        if hasattr(selfattr, "compare"):
            compval, compwhich = selfattr.compare(otherattr)
        elif hasattr(otherattr, "compare"):
            compval, compwhich = otherattr.compare(selfattr)
        if compval is not None and not compval and compwhich == Comparison.EqualOrUnclear:
            return compval, default_compare
        elif compval is not None:
            return compval, compwhich

        if _both_none(selfattr, otherattr):
            return True, Comparison.BothInvalid
        if (isinstance(selfattr, str)
            and isinstance(otherattr, str)
                and len(selfattr.strip()) == 0 and len(otherattr.strip()) == 0):
           return True, Comparison.BothInvalid
        if selfattr != otherattr:
            if selfattr is None:
                if isinstance(otherattr, str) and len(otherattr.strip()) == 0:
                    return True, Comparison.BothInvalid
                return False, Comparison.Right
            if otherattr is None:
                if isinstance(selfattr, str) and len(selfattr.strip()) == 0:
                    return True, Comparison.BothInvalid
                return False, Comparison.Left
            if isinstance(selfattr, str) and isinstance(otherattr, str):
                if _isnull(selfattr):
                    if _isnull(otherattr):
                        return True, Comparison.BothInvalid
                    return False, Comparison.Right
                elif _isnull(otherattr):
                    return False, Comparison.Left
                return False, default_compare
            elif isinstance(selfattr, collections.Iterable) and isinstance(otherattr, collections.Iterable):
                if len(selfattr) and len(otherattr):
                    return False, default_compare
                elif len(selfattr):
                    return False, Comparison.Left
                elif len(otherattr):
                    return False, Comparison.Right
                else:
                    return True, Comparison.BothInvalid
            elif isinstance(selfattr, bool) or isinstance(otherattr, bool):
                if selfattr is None:
                    return False, Comparison.Right
                elif otherattr is None:
                    return False, Comparison.Left
                if len(str(selfattr)) == 0:
                    return False, Comparison.Right
                elif len(str(otherattr)) == 0:
                    return False, Comparison.Left
                else:
                    return False, default_compare
            else:
                return False, default_compare
        return True, Comparison.EqualOrUnclear

    def compare(self, other):
        bad = {}
        roots = {}
        single_root_flds = []
        multiple_root_flds = []
        skip_fields = []
        # base preference on which was updated first in the absence of anything else
        # (like a field considering a type primary)
        preferred_comparison = Comparison.EqualOrUnclear
        if self.lmoddt is None:
            preferred_comparison = Comparison.Right
        elif other.lmoddt is None:
            preferred_comparison = Comparison.Left
        elif self.lmoddt > other.lmoddt:
            preferred_comparison = Comparison.Left
        else:
            preferred_comparison = Comparison.Right
        for fld in attr.fields(self.__class__):
            attrname = fld.name
            if attrname[0] == "_":
                continue
            if attrname == "lmoddt":
                continue
            if attrname == "createddt":
                continue
            root, num = Contact.get_field_parts(attrname)
            if root not in roots:
                roots[root] = []
            roots[root].append({"root": root, "num": num, "orig": attrname})

        for root, rootds in roots.items():
            if len(rootds) > 1:
                multiple_root_flds.append(root)
            else:
                single_root_flds.append(root)

        for root in multiple_root_flds:
            flds = roots[root]
            for fld1 in flds:  # left
                found_equal = False
                comparisons = []
                fldname1 = fld1["orig"]
                if fldname1 in skip_fields:
                    continue
                selfattr = getattr(self, fldname1, None)
                # if ANY other fld matches, then consider it OK
                for fld2 in flds:  # right
                    fldname2 = fld2["orig"]
                    otherattr = getattr(other, fldname2)
                    res, which = Contact._compare_attr(selfattr, otherattr, default_compare=preferred_comparison)
                    comparisons.append(which)
                    if res and which != Comparison.BothInvalid:
                        found_equal = True
                        skip_fields.append(fldname2)
                if not found_equal and not all([x == Comparison.BothInvalid for x in comparisons]):
                    # just shunt it to the next check - easiest
                    single_root_flds.append(fldname1)

        for attrname in single_root_flds:
            selfattr = getattr(self, attrname, None)
            otherattr = getattr(other, attrname, None)
            if selfattr != otherattr:
                if self.is_primary(attrname):
                    if not other.is_primary(attrname):
                        bad[attrname] = Comparison.Left
                        continue
                elif other.is_primary(attrname):
                    bad[attrname] = Comparison.Right
                    continue
            res, which = Contact._compare_attr(selfattr, otherattr, default_compare=preferred_comparison)
            if not res:
                bad[attrname] = which

        final = {}
        for attrname, comp in bad.items():
            selfattr = getattr(self, attrname, None)
            otherattr = getattr(other, attrname, None)
            final[attrname] = f"[{selfattr}] [{otherattr}]"
        return len(bad) == 0, bad, final

    def shunt(self, fld, val):
        """Move primary to secondary (e.g. haddr -> h2addr)"""
        def _get_shunt_fld(fld):
            return ({"haddr": "h2addr", "email1": "email2",
                     "child1": "child2", "child2": "child3",
                     "child3": "child4", "mobilephone": "mobile2phone",
                     "mobile2phone": "mobile3phone", "homephone": "home2phone",
                     "workphone": "work2phone", "otherphone": "other2phone"}
                    .get(fld, None))

        shunt_fld = _get_shunt_fld(fld)
        if shunt_fld is None:
            return False
        shunt_fld_val = getattr(self, shunt_fld, None)
        if shunt_fld_val is not None:
            return False
        setattr(self, shunt_fld, val)
        return True

    @classmethod
    def resolve(cls, c1, c2, take_ids=Comparison.Right):
        unresolved = []
        changed = {}
        ids_c = c1
        if take_ids == Comparison.Right:
            ids_c = c2
        cout = attr.evolve(c1)
        for fld in attr.fields(cls):
            if fld.name[0] != "_" and fld.name not in ids_c.ids():
                continue
            setattr(cout, fld.name, getattr(ids_c, fld.name))
        _, comparisons, _ = c1.compare(c2)
        for fld, which in comparisons.items():
            if which == Comparison.Right:
                setattr(cout, fld, getattr(c2, fld))
                changed[fld] = getattr(c2, fld)
            if which == Comparison.EqualOrUnclear:
                result = cout.shunt(fld, getattr(c2, fld))
                if not result:
                    unresolved.append(fld)
        return cout, changed, unresolved
