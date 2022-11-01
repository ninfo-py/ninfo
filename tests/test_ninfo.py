import ninfo
from tests.common import Wrapper

def test_plugin_loading():
    test_plugins = {
        "a": Wrapper("tests.plug_a"),
    }
    n=ninfo.Ninfo(plugin_modules=test_plugins)
    assert 'a' in n
    assert 'b' not in n

    plugin = n.get_plugin('a')
    assert plugin is not None

    plugin = n.get_plugin('b')
    assert plugin is None

def test_plugin_lazy_loading():
    test_plugins = {
        "a": Wrapper("tests.plug_a"),
    }
    n=ninfo.Ninfo(plugin_modules=test_plugins)
    assert 'a' in n
    assert 'a' not in n.plugin_instances

    plugin = n.get_plugin('a')
    assert plugin is not None
    assert 'a' in n.plugin_instances

def test_plugin_lazy_init():
    test_plugins = {
        "a": Wrapper("tests.plug_a"),
    }
    n=ninfo.Ninfo(plugin_modules=test_plugins)
    plugin = n.get_plugin('a')
    assert plugin is not None
    assert 'a' in n.plugin_instances

    assert plugin.initialized is False

    res = n.get_info("a", "example.com")
    assert plugin.initialized is True

    assert res == "AAAAAAAAAAA"

def test_plugin_compatible_types():
    test_plugins = {
        "a": Wrapper("tests.plug_a"),
    }
    n=ninfo.Ninfo(plugin_modules=test_plugins)

    cases = [
        ("example.com", True),
        ("1.2.3.4", True),
        ("00:11:22:33:44:55", False),
    ]
    for arg, expected in cases:
        yield _plugin_compatible_type_case, n, arg, expected

def _plugin_compatible_type_case(n, arg, expected):
    assert n.compatible_argument("a", arg) == expected
