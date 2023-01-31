import ieeemac
import IPy
import re


def isip(arg):
    """is arg an ip address?"""
    try:
        x = IPy.IP(arg)
        return x.version()
    except ValueError:
        return False


_hash_re = re.compile("^[0-9a-fA-F]+$")


def ishash(arg):
    return bool(_hash_re.match(arg))


def get_type(arg):
    """Return a list of possible types for the type of the
    argument (mac, ip, hostname, url,hostport, and/or username)"""

    potential_types = []

    ip_types = {
        (4, False): "ip",
        (6, False): "ip6",
        (4, True): "cidr",
        (6, True): "cidr6",
    }

    if ieeemac.ismac(arg):
        potential_types.append("mac")
    # macs can look like hashes, so check them first
    if ishash(arg):
        potential_types.append("hash")
    ipver = isip(arg)
    if ipver:
        potential_types.append(ip_types[(ipver, "/" in arg)])

    parts = arg.split(":")
    if "://" in arg:
        potential_types.append("url")
    elif len(parts) == 2 and parts[1].isdigit():
        potential_types.append("hostport")
    elif "." in arg and not ipver:
        potential_types.append("hostname")

    potential_types.append("username")

    return potential_types


def is_local(networks, ip):
    """Return True if `ip` is in `networks`"""
    for n in networks:
        if ip in n:
            return True
    return False


def parse_query(s):
    """Split the query up into arguments and options
    This should be easy to do using a regex, but I can't figure it out.
    so, state machine it is."""

    args = []
    options = {}

    # regex too complicated, state machine easy
    # first split the string into components, respecting quotes
    parts = []
    in_quote = False
    p = ""
    for l in s:
        if l.isspace() and not in_quote:
            parts.append(p)
            p = ""
        elif l in "\"'" and not in_quote:
            in_quote = l
        elif l == in_quote:
            in_quote = False
        else:
            p += l
    if p:
        parts.append(p)

    # now separate each argument or option
    for arg in parts:
        if "=" in arg and "//" not in arg:  # has a = but doesn't look like a URL
            k, v = arg.split("=", 1)
            v = v.strip('"')  # remove the quotes
            options[k] = v
        else:
            args.append(arg)
    return args, options


def fmt_dict_array(ar, order=None, header=True):
    # allow for an empty array
    # if the array is empty and no order is paseed, return ""
    # otherwise generate just the header
    if not ar:
        if not order:
            return ""
        first = dict([(x, x) for x in order])
    else:
        first = ar[0]
    if header:  # insert a new row of just the keys, the next loop will do the rest
        new = dict([(x, str(x).capitalize()) for x in first.keys()])
        new = [new]
    else:
        new = []
    # figure out what the longest column in each row is
    maxes = dict([(a, len(str(b))) for a, b in first.items()])
    for x in new + ar:
        for k, v in x.items():
            size = len(str(v))
            if size > maxes[k]:
                maxes[k] = size

    maxesfmt = dict([(x, "%%-%ds" % (y + 1)) for x, y in maxes.items()])
    if order:
        it = order
    else:
        it = first  # will iterate over the keys however

    table = []

    for x in new + ar:
        row = []
        for c in it:
            row.append(maxesfmt[c] % x[c])
        line = " ".join(row).strip()
        table.append(line)

    return "\n".join(table)


def unique(lst):
    out = []
    seen = set()
    for x in lst:
        if x not in seen:
            out.append(x)
            seen.add(x)
    return out
