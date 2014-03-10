% nInfo: Query all the Things
% Justin Azoff
% March 10, 2014

# nInfo: Query all the Things

![](../meme.jpeg "Query all the Things")

# What is nInfo?

- nInfo is a Library
- nInfo is a CLI Tool
- nInfo is a Web Interface

# What is nInfo?

- nInfo is an API for your APIs
- nInfo is an API for external APIs
- nInfo is an API for things that don't really have an API

# Why nInfo?

nInfo provides a *uniform* API for looking up data

. . .

that caches results

. . .

and has single point of configuration

. . .

and comes with a nice web interface


# What does nInfo Look like?

## Used as a Library

~~~~~~~~~~~~~~~~~~ {.python}
>>> from ninfo import Ninfo
>>> n = Ninfo()
>>> print n.get_info_text("geoip", "1.2.3.4")
AU - Australia
>>> print n.get_info("geoip", "1.2.3.4")["country_name"]
Australia
~~~~~~~~~~~~~~~~~~

# What does nInfo Look like?

## Used as a CLI Tool

~~~~~~~~~~~~~~~~~~
$ ninfo -p geoip 1.2.3.4 4.2.2.2
=== 1.2.3.4 ===
*** GeoIP (Geographic IP location) ***
AU - Australia

=== 4.2.2.2 ===
*** GeoIP (Geographic IP location) ***
US - United States
~~~~~~~~~~~~~~~~~~

# What does nInfo Look like?

## Web Interface

Demo time :-)

# Plugin Meta Data

~~~~~~~~~~~~~~~~~~ {.python}

from ninfo import PluginBase

class shodan_plug(PluginBase):
    """This plugin returns any information from Shodan"""
    name    =    'shodan'
    title   =    'Shodan'
    description   =  'Computer Search Engine'
    cache_timeout   =  60*60*2
    types   =    ['ip']
    remote = False

    #<<Magic Here>>

plugin_class = shodan_plug

~~~~~~~~~~~~~~~~~~

# Setup function

~~~~~~~~~~~~~~~~~~ {.python}
    def setup(self):
        from shodan import WebAPI
        self.api = WebAPI(self.plugin_config["api_key"])

~~~~~~~~~~~~~~~~~~

# Get Info function
~~~~~~~~~~~~~~~~~~ {.python}
    def get_info(self, arg):
        info = self.api.host(arg)
        return info
~~~~~~~~~~~~~~~~~~
