"""Requires splunky and the following in the ninfo config:

[splunk]
host = splunk-backend.example.com
web = splunk-head.example.com
port = 8089
username = infosearch
password = password_for_info_to_use
"""

from ninfo import PluginBase

import logging
logger = logging.getLogger(__name__)

class SplunkBase(PluginBase):
    """This plugin is a base that can be used for splunk searches
    
    subclass it and override 'TEMPLATE' or get_info
    """
    TEMPLATE = None
    def setup(self):
        import splunky
        sc = self.config['splunk']
        host = sc['host']
        port = sc['port']
        username = sc['username']
        password = sc['password']
        self.s = splunky.Server(host=host, port=port, username=username, password=password)

    def get_info(self, arg):
        if not self.TEMPLATE:
            raise NotImplementedError("You must override self.TEMPLATE or self.get_info")

        query = self.TEMPLATE % arg
        logger.debug("Searching splunk for '%s'" % query)
        events = self.s.search_sync(query)
        return {'events': events}


