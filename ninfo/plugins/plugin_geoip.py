import GeoIP
from ninfo import util
from ninfo import PluginBase

class geoip(PluginBase):
    def setup(self):
        self.g=GeoIP.new(GeoIP.GEOIP_STANDARD)

    def get_info(self, ip):
        code = self.g.country_code_by_addr(ip)
        name = self.g.country_name_by_addr(ip)
        return dict(code=code, name=name)

    get_info_json = get_info

plugin = {
    'name':         'geoip',
    'title':        'geoip',
    'description':  'geoip',
    'class'      :  geoip,
    'longdescription': 'This plugin returns the location of this ip',
    'cachetimeout':  60*60,
    'types':    ['ip'],
    'local':    False,
}
