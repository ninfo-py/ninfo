import ninfo
def test_loading():
    n = ninfo.Ninfo()

    assert n.plugin_modules != {}

    assert 'whois' not in n.plugins
    assert 'whois' not in n.plugin_instances

    n.get_plugin('whois')

    assert 'whois' in n.plugins

    n.get_inst('whois')
    assert 'whois' in n.plugin_instances
