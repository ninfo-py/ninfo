import ieeemac
import IPy
import re

def isip(arg):
    """is arg an ip address?"""
    try:
        IPy.IP(arg)
        return True
    except ValueError:
        return False

def get_type(arg):
    if ieeemac.ismac(arg):
        return 'mac'
    if isip(arg):
        return 'ip'
    if '.' in arg:
        return 'hostname'
    
    return 'username'

def is_local(networks, ip):
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
    #split into words OR key:value OR key:"value value"
    #re matches (words|key:value|key:"value value")
    parts = [x[1] or x[0] for x in re.findall('((\w+)(?: |$)|\w+:\w+|\w+:"[^"]+")', s)]
    for arg in parts:
        if ":" not in arg:
            args.append(arg)
        else:
            k, v = arg.split(":", 1)
            v = v.strip('"') # remove the quotes
            options[k] = v
    return args, options
