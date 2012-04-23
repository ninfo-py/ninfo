import GeoIP
from ninfo import util
from ninfo import PluginBase
import os

class geoip(PluginBase):
    """This plugin returns the location of this ip"""

    name = "geoip"
    title = "GeoIP"
    description = "GeoIP"
    cache_timeout = None
    types = ['ip']
    local = False

    def setup(self):
        self.g=GeoIP.new(GeoIP.GEOIP_STANDARD)

    def get_info(self, ip):
        code = self.g.country_code_by_addr(ip)
        name = self.g.country_name_by_addr(ip)
        return dict(code=code, name=name)

plugin_class = geoip
