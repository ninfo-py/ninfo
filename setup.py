from setuptools import setup, find_packages

setup(name='ninfo',
    version='0.9.0',
    zip_safe=False,
    description="Plugin based information gathering library",
    packages = find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "Mako",
        "python-memcached",
        "ieeemac",
        "IPy",
    ],
    extras_require = {
        'Splunk' : ['splunk-sdk'],
    },
    entry_points = {
        'console_scripts': [
            'ninfo = ninfo:main',
        ]
    }
)
