#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup


setup(
    name='interssection',
    version='0.1.0',
    description='treat Atom and RSS feeds like sets',
    author='Maciej Konieczny',
    author_email='hello@narf.pl',
    url='http://github.com/narfdotpl/interssection',
    packages=['interssection', 'interssection.templates'],
    package_data={'interssection.templates': ['*.xml']},
    install_requires=['Jinja2==2.5.2', 'feedparser==5.1.2']
)
