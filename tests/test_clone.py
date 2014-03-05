import ninfo
from tests.common import Wrapper
from nose.tools import eq_

test_plugins = {
    "a": Wrapper("tests.plug_a"),
}

def test_plugin_cloning_no_config():
    n=ninfo.Ninfo(plugin_modules=test_plugins)
    assert 'a' in n
    assert 'b' not in n

def test_plugin_cloning_with_config():
    n=ninfo.Ninfo(plugin_modules=test_plugins, config_file="tests/clone.cfg")
    assert 'a' in n
    assert 'b' in n

def test_plugin_cloning_cloned_config():
    n=ninfo.Ninfo(plugin_modules=test_plugins, config_file="tests/clone.cfg")
    a = n.get_plugin('a')
    b = n.get_plugin('b')

    eq_(a.plugin_config, {"one": '1', "two": '2'})
    eq_(b.plugin_config, {"clone": 'a', "one": 'one', "two": '2', "three": '3'})
