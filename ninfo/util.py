import ieeemac
import re
import IPy

ipregex = r"(?P<ip>((25[0-5]|2[0-4]\d|[01]\d\d|\d?\d)\.){3}(25[0-5]|2[0-4]\d|[01]\d\d|\d?\d))$"
ipregex = re.compile(ipregex)
def isip(arg):
    """is arg an ip address?"""
    return bool(ipregex.match(str(arg)))

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
