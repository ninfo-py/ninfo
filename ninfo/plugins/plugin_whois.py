from ninfo import PluginBase
from subprocess import Popen, PIPE

class whois(PluginBase):
    def get_info(self, arg):
        pipe = Popen(["whois", arg], stdout=PIPE)
        output = pipe.communicate()[0]
        status = pipe.returncode

        output = output.decode('ascii','ignore')
        return dict(status=status,output=output)

plugin = {
    'name':         'whois',
    'title':        'whois',
    'description':  'whois',
    'class'      :  whois,
    'longdescription': 'This plugin returns the output of the whois program for this ip',
    'cachetimeout':  60*60,
    'types':    ['ip','hostname'],
    'local':    False,
}
