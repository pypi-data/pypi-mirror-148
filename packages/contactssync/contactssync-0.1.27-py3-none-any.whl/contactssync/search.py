
import attr
import collections
from typing import Dict, List

from .base import Contact
from .nicknames import get_nicknames, get_fullnames


def _check_duplicate_contact(c1, c2):
    comparison, _, _ = c1.compare(c2)
    if comparison:
        return True
    return False

@attr.s(auto_attribs=True)
class Search:
    contacts: List[Contact] = None
    _by_ln: Dict[str, List[Contact]] = None
    _by_fn: Dict[str, List[Contact]] = None
    _by_ln_nn: Dict[str, List[Contact]] = None
    _by_id: Dict[str, Contact] = None
    _by_foreign_id: Dict[str, Dict[str, Contact]] = None
    _skip_duplicates: bool = True

    def __len__(self):
        return len(contacts)

    def __iter__(self):
        return self.contacts.__iter__()

    def _complain_about_unmatching_duplicate(self, orig, dup):
        if self._skip_duplicates:
            return
        raise Exception(
            f"found two contacts with id {dup._id}.  We would "
            f"treat as duplicates and skip, but the contacts "
            f"do not match.   You should review.  The contacts are: "
            f"EXISTING:\n{orig}\n"
            f"NEW:\n{dup}"
        )

    def _add_individual_contact(self, c):
        if c.ln is not None and len(c.ln):
            if c.ln.lower() not in self._by_ln:
                self._by_ln[c.ln.lower()] = []
            self._by_ln[c.ln.lower()].append(c)

        if c.fn is not None and len(c.fn):
            if c.fn.lower() not in self._by_fn:
                self._by_fn[c.fn.lower()] = []
            self._by_fn[c.fn.lower()].append(c)

        if c._id is not None and len(c._id):
            if c._id in self._by_id:
                _existing = self._by_id[c._id]
                if not _check_duplicate_contact(_existing, c):
                    self._complain_about_nonmatching_duplicate(_existing, c)
            self._by_id[c._id] = c

        foreign_id_name = getattr(c, "ids")()[0]
        foreign_id = c._id
        if foreign_id_name not in self._by_foreign_id:
            self._by_foreign_id[foreign_id_name] = {}

        foreign_id_dict = self._by_foreign_id[foreign_id_name]
        if foreign_id in foreign_id_dict:
            _existing = foreign_id_dict[c._id]
            if not _check_duplicate_contact(_existing, c):
                self._complain_about_nonmatching_duplicate(_existing, c)
        foreign_id_dict[c._id] = c

    def _populate(self):
        for c in self.contacts:
            self._add_individual_contact(c)

    def __attrs_post_init__(self):
        if self.contacts is None:
            self.contacts = []
        self._by_ln = {}
        self._by_fn = {}
        self._by_id = {}
        self._by_foreign_id = {}
        self._populate()

    def add(self, cs):
        if cs is None:
            return 0
        if not isinstance(cs, collections.Iterable):
            cs = [cs]
        for c in cs:
            self._add_individual_contact(c)

    def by_ln(self, ln):
        if ln is None:
            return []
        lnlower = ln.lower()
        if lnlower not in self._by_ln:
            return []
        return self._by_ln[lnlower]

    def by_fn(self, fn):
        if fn is None:
            return []
        fnlower = fn.lower()
        if fnlower not in self._by_fn:
            return []
        return self._by_fn[fnlower]

    def by_id(self, id_):
        if id_ not in self._by_id:
            return None
        return self._by_id[id_]

    def find_by_name(self, fn, ln, nn=None):
        matching = []
        if ln is None or len(ln) == 0:
            return self.by_fn(fn)
        cs = self.by_ln(ln)
        for c in cs:
            if fn is None and c.fn is None:
                matching.append(c)
                continue
            elif fn is None:
                continue
            elif c.fn is None:
                continue
            elif fn.lower() == c.fn.lower():
                matching.append(c)
        if nn is not None:
            nnlower = nn.lower()
            for c in cs:
                if c.fn is None:
                    continue
                if nnlower == c.fn.lower():
                    matching.append(c)
                elif c.nn is not None and nnlower == c.nn.lower():
                    matching.append(c)
        return matching

    def find(self, c_, add_nicknames=True):
        if c_ is None:
            return []
        # for women/maiden names
        middle_name = c_.mn
        nicknames = set()
        firstnames = get_fullnames(c_.fn)
        if firstnames is None:
            firstnames = [ c_.fn ]
        else:
            firstnames.append(c_.fn)
        if c_.nn is not None:
            nicknames.add(c_.nn)
        if add_nicknames:
            general_nicknames = get_nicknames(c_.fn)
            if general_nicknames is not None:
                nicknames.update(set(general_nicknames))
        if len(nicknames) == 0:
            nicknames.add(None)
        results = set()
        for fn in firstnames:
            for nn in nicknames:
                results.update(self.find_by_name(fn, c_.ln, nn))
        # try with various maiden name combos
        lns_to_try = []
        if c_.ln is not None:
            lns_to_try = c_.ln.replace("-", " ").split(" ")
        if middle_name is not None and len(middle_name):
            lns_to_try.extend([
                middle_name,
                f"{middle_name}-{c_.ln}",
                f"{middle_name} {c_.ln}"
            ])
        if len(lns_to_try) > 1:
            for ln in lns_to_try:
                for nn in nicknames:
                    results.update(self.find_by_name(c_.fn, ln, nn))
        return list(results)
