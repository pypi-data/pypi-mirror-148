
from pathlib import Path

_NICKNAMES = {}
_FULLNAMES = {}

def _load_nicknames():
    names_file = Path(__file__).parent / "__data__" / "names.csv"
    with names_file.open() as nf:
        lines = nf.readlines()
    for line in lines:
        names = line.strip().split(",")
        fullname = names[0].lower()
        nicknames = [name.lower() for name in names[1:]]
        _NICKNAMES[fullname] = nicknames
        for nn in nicknames:
            if nn not in _FULLNAMES:
                _FULLNAMES[nn] = set()
            _FULLNAMES[nn].add(fullname)

def get_nicknames(name):
    if len(_NICKNAMES) == 0:
        _load_nicknames()
    if name is None or not isinstance(name, str):
        return None
    return _NICKNAMES.get(name.lower(), [])

def get_fullnames(nickname):
    if len(_FULLNAMES) == 0:
        _load_nicknames()
    if nickname is None or not isinstance(nickname, str):
        return None
    return list(_FULLNAMES.get(nickname.lower(), []))
