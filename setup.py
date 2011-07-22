from distutils.core import setup
from glob import glob

setup(name='ninfo',
    version='0.1.0',
    zip_safe=False,
    packages = ['ninfo', 'ninfo.plugins'],
    package_data = { '': ['*.mako'] },
    install_requires=[
        "Mako",
        "python-memcached",
        "ieeemac",
        "IPy",
    ],
    entry_points = {
        'console_scripts': [
            'ninfo-main = ninfo:main',
        ],
        'ninfo.plugin': [
            'whois = ninfo.plugins.plugin_whois',
            'geoip = ninfo.plugins.plugin_geoip',
        ]
    }
) 
