from setuptools import setup, find_packages

setup(name='ninfo',
    version='0.2.0',
    zip_safe=False,
    packages = find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "Mako",
        "python-memcached",
        "ieeemac",
        "cymruwhois",
        "IPy",
    ],
    entry_points = {
        'console_scripts': [
            'ninfo = ninfo:main',
        ],
        'ninfo.plugin': [
            'whois = ninfo.plugins.whois_plugin',
            'geoip = ninfo.plugins.geoip_plugin',
            'cymruwhois = ninfo.plugins.cymruwhois_plugin',
        ]
    }
) 
