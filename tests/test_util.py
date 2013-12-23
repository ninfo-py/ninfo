from nose.tools import eq_
from ninfo import util
def test_is_ip():
    cases = (
        ("1.2.3.4", 4),
        ("123.123.123.123", 4),
        ("123.123.123.321", False),
        ("1.2.3.4a", False),
        ("a1.2.3.4", False),
        ("blah", False),
    )

    for ip, valid in cases:
        yield ip_case, ip, valid

def ip_case(ip, valid):
    eq_(util.isip(ip), valid)

def test_get_type():
    cases = (
        ("1.2.3.4", "ip"),
        ("2001:4860:800e::69", "ip6"),
        ("001122334455", "mac"),
        ("blah.com", "hostname"),
        ("blah", "username"),
        ("1.2.3.0/24", "cidr"),
        ("2001:4860:800e::0/48", "cidr6"),
    )
    for x, t in cases:
        yield type_case, x, t

def type_case(x, expected_type):
    eq_(util.get_type(x), expected_type)


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


def test_query_parsing():
    cases = (
        ('one two', (['one', 'two'], {})),
        ('arg key=value', (['arg'], {'key': 'value'})),
        ('one two key=value', (['one','two'], {'key': 'value'})),
        ('one two key=value b=c', (['one','two'], {'key': 'value', 'b': 'c'})),
        ('arg key="spaced value"', (['arg'], {'key': 'spaced value'})),
        ('arg two key="spaced value" b="c d"', (['arg','two'], {'key': 'spaced value', 'b': "c d"})),
        ('1.2.3.4', (['1.2.3.4'], {})),
        ('1.2.3.4 time="2012-04-19 11:50"', (['1.2.3.4'], {'time':'2012-04-19 11:50'})),
        ('1.2.3.4 time="2012-04-19 11:50:22"', (['1.2.3.4'], {'time':'2012-04-19 11:50:22'})),
        ('00:11:22:33:44:55', (['00:11:22:33:44:55'], {})),
        ('http://example.com', (['http://example.com'], {})),
    )

    for input, output in cases:
        yield query_parse_case, input, output

def query_parse_case(input, output):
    assert util.parse_query(input) == output, "%r != %r" % (util.parse_query(input), output)

def test_unique():
    cases = (
        (['a','a'], ['a']),
        (['a','b','a'], ['a','b']),
    )
    for input, output in cases:
        yield unique_case, input, output

def unique_case(input, output):
    assert util.unique(input) == output
