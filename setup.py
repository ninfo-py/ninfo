from setuptools import setup, find_packages

setup(name='ninfo',
    version='0.3.1k',
    zip_safe=False,
    packages = find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "Mako",
        "python-memcached",
        "ieeemac",
        "cymruwhois",
        "IPy",
        "pygeoip",
    ],
    extras_require = {
        'Splunk' : ['splunk-sdk'],
    },
    entry_points = {
        'console_scripts': [
            'ninfo = ninfo:main',
        ],
        'ninfo.plugin': [
            'cymruwhois = ninfo.plugins.cymruwhois_plugin',
        ]
    }
)
