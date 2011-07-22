from distutils.core import setup
from glob import glob

setup(name='ninfo',
    version='0.1.0',
    zip_safe=False,
    packages = ['ninfo', 'ninfo.plugins'],
    install_requires=[
        "Mako",
        "python-memcached",
        "ieeemac",
        "cymruwhois",
        "IPy",
    ],
    entry_points = {
        'console_scripts': [
            'ninfo-main = ninfo:main',
        ],
        'ninfo.plugin': [
            'whois = ninfo.plugins.whois_plugin',
            'geoip = ninfo.plugins.geoip_plugin',
            'cymruwhois = ninfo.plugins.cymruwhois_plugin',
        ]
    }
) 
