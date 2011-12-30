from ninfo import util
def test_is_ip():
    cases = (
        ("1.2.3.4", True),
        ("123.123.123.123", True),
        ("123.123.123.321", False),
        ("1.2.3.4a", False),
        ("a1.2.3.4", False),
        ("blah", False),
    )

    for ip, valid in cases:
        yield ip_case, ip, valid

def ip_case(ip, valid):
    assert util.isip(ip) == valid

def test_get_type():
    cases = (
        ("1.2.3.4", "ip"),
        ("2001:4860:800e::69", "ip"),
        ("001122334455", "mac"),
        ("blah.com", "hostname"),
        ("blah", "username"),
    )
    for x, t in cases:
        yield type_case, x, t

def type_case(x, expected_type):
    assert util.get_type(x) == expected_type


import IPy
def test_is_local():
    networks = ["192.168.1.0/24","192.168.99.0/24"]
    networks = [IPy.IP(n) for n in networks]

    cases = (
        ("1.2.3.4", False),
        ("192.168.1.33", True),
        ("192.168.99.33", True),
        ("192.168.100.33", False),
    )

    for ip, result in cases:
        yield is_local_case, networks, ip, result

def is_local_case(networks, ip, result):
    assert util.is_local(networks, ip) == result
