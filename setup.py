#!/usr/bin/env python

from setuptools import setup

setup(
    name = "mockldap3",
    version = "0.0.1",
    url = 'http://github.com/liut/mockldap3',
    license = '',
    description = "Mock LDAP for ldap3",
    author = 'Eagle Liut',
    packages = ['mockldap3'],
    keywords=['mock', 'ldap', 'ldap3'],
    install_requires=[
        'setuptools',
        'ldap3',
    ],

)

