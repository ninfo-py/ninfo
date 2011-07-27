import ieeemac
import IPy

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
