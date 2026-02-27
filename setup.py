from setuptools import setup, find_packages

setup(name='ninfo',
    version='1.0.1',
    zip_safe=False,
    description="Plugin based information gathering library",
    packages = find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "Mako",
        "python-memcached",
        "ieeemac",
        "IPy",
        "importlib-metadata>=3.6.0; python_version < '3.10'",
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
