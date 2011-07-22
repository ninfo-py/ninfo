from ninfo import PluginBase
from subprocess import Popen, PIPE

class whois(PluginBase):
    name =         'whois'
    title =        'whois'
    description =  'whois'
    long_description =  'This plugin returns the output of the whois program for this ip'
    cache_timeout =   60*60
    types =     ['ip','hostname']
    local =     False

    def get_info(self, arg):
        pipe = Popen(["whois", arg], stdout=PIPE)
        output = pipe.communicate()[0]
        status = pipe.returncode

        output = output.decode('ascii','ignore')
        return dict(status=status,output=output)

plugin_class = whois
