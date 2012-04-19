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

    #regex too complicated, state machine easy
    #first split the string into components, respecting quotes
    parts = []
    in_quote = False
    p = ""
    for l in s:
        if l.isspace() and not in_quote:
            parts.append(p)
            p=""
        elif l in '"\'' and not in_quote:
            in_quote = l
        elif l == in_quote:
            in_quote = False
        else:
            p+=l
    if p:
        parts.append(p)

    #now separate each argument or option
    for arg in parts:
        if 1 <= arg.count(":") <= 2 and "//" not in arg:
            k, v = arg.split(":", 1)
            v = v.strip('"') # remove the quotes
            options[k] = v
        else:
            args.append(arg)
    return args, options
