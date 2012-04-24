import GeoIP
from ninfo import util
from ninfo import PluginBase
import os

CITY_DB = "/usr/share/GeoIP/GeoLiteCity.dat"
record_keys = ['city', 'region_name', 'region', 'area_code', 'time_zone', 'longitude', 'metro_code', 'country_code3', 'latitude', 'postal_code', 'dma_code', 'country_code', 'country_name']


class geoip(PluginBase):
    """This plugin returns the location of this ip"""

    name = "geoip"
    title = "GeoIP"
    description = "GeoIP"
    cache_timeout = None
    types = ['ip']
    local = False

    def setup(self):
        if os.path.exists(CITY_DB):
            self.city = True
            self.g=GeoIP.open(CITY_DB, 0)
        else:
            self.city = False
            self.g=GeoIP.new(GeoIP.GEOIP_STANDARD)


    def get_info(self, ip):
        if self.city:
            record = self.g.record_by_addr(ip)
        else:
            record = dict.fromkeys(record_keys, None)
            record['country_code'] = self.g.country_code_by_addr(ip)
            record['country_name'] = self.g.country_name_by_addr(ip)

        return record

plugin_class = geoip
