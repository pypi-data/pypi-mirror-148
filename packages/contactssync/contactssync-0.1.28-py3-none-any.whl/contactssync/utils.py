
from collections import defaultdict
import itertools
import re

def _chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def _both_none(left, right):
    if left is None and right is None:
        return True
    return False

def _rowget(row,val,defval = None, deftype = None):
    val = row.get(val,defval)
    if deftype is not None and val is not None:
        return deftype(val)
    return val

def _str_not_none(s):
    if s is None:
        return ""
    return s

def _strip_bad_chars(s):
    if s is None:
        return None
    return re.sub(r"[^a-zA-Z0-9^_^\-^\s^&^+^\<^\>^\[^\]^\(^\)^|^#^\/^\'\.\@]", "", s).rstrip('\x00')

def _tolower(s):
    return _str_not_none(s).lower()

def _get_dates_from_list(l, t):
    _listout = [x for x in itertools.takewhile(lambda d: d.get("type", "") != t, l)]
    val = ""
    if len(_listout):
        val = str(_listout[0]['year'] * 10000 + _listout[0]['month']*100 + _listout[0]['day'])
    return val

def _make_dict_from_list(l_of_d, keyname="type", valname="value", error_on_missing=True):
    outdict = {}
    already_used = defaultdict(lambda x: 0)
    for x in l_of_d:
        key = x.get(keyname, "Unknown")
        if not error_on_missing:
            val = x.get(valname,None)
        else:
            val = x[valname]
        if key in already_used:
            num_used = already_used[key]
            num_used += 1
            already_used[key] = num_used
            outdict[f"{key}{num_used}"] = val
        else:
            outdict[key] = val
            already_used[key] = 1
    return outdict

def _date_to_ymd(s):
    try:
        date = int(s)
        y = int(date/10000)
        m = int((date - y*100)/100)
        d = date - y*10000 - m*10
        return y,m,d
    except Exception:
        try:
            y = int(s[0:4])
            m = int(s[5:7])
            d = int(s[8:10])
            return y,m,d
        except Exception:
            try:
                y = int(s[6:10])
                m = int(s[0:2])
                d = int(s[3:5])
                return y,m,d
            except Exception:
                return 0,0,0
