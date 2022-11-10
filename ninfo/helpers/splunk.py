"""Requires the splunk-sdk and the following in the ninfo config:

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
        import splunklib.client as client
        import splunklib.results as results

        self.client = client
        self.splunklibresults = results

    def connect(self):
        sc = self.config["splunk"]
        host = sc["host"]
        port = sc["port"]
        username = sc["username"]
        password = sc["password"]
        self.s = self.client.connect(
            host=host, port=port, username=username, password=password
        )

    def do_search(self, query):
        self.connect()
        logger.debug("Searching splunk for '%s'" % query)
        q = "search " + query
        rr = self.splunklibresults.ResultsReader(self.s.jobs.export(q))
        events = []
        for result in rr:
            if isinstance(result, self.splunklibresults.Message):
                # Diagnostic messages may be returned in the results
                logger.debug("%s: %s" % (result.type, result.message))
            elif isinstance(result, dict):
                # Normal events are returned as dicts
                events.append(result)
        return events

    def get_info(self, arg):
        if not self.TEMPLATE:
            raise NotImplementedError(
                "You must override self.TEMPLATE or self.get_info"
            )

        query = self.TEMPLATE % arg
        events = self.do_search(query)
        return {"events": events}
