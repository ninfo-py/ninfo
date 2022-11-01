import ninfo
from tests.common import Wrapper

def test_plugin_cloning_no_config():
    test_plugins = {
        "a": Wrapper("tests.plug_a"),
    }
    n=ninfo.Ninfo(plugin_modules=test_plugins)
    assert 'a' in n
    assert 'b' not in n

def test_plugin_cloning_with_config():
    test_plugins = {
        "a": Wrapper("tests.plug_a"),
    }
    n=ninfo.Ninfo(plugin_modules=test_plugins, config_file="tests/clone.cfg")
    assert 'a' in n
    assert 'b' in n

def test_plugin_cloning_cloned_config():
    test_plugins = {
        "a": Wrapper("tests.plug_a"),
    }
    n=ninfo.Ninfo(plugin_modules=test_plugins, config_file="tests/clone.cfg")
    a = n.get_plugin('a')
    b = n.get_plugin('b')

    assert a.plugin_config == {"one": '1', "two": '2'}
    assert b.plugin_config == {"clone": 'a', "one": 'one', "two": '2', "three": '3'}
