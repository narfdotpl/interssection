#!/usr/bin/env python
# encoding: utf-8

from jinja2 import Environment, PackageLoader


__all__ = ['render_as_atom']


# create environment
env = Environment(loader=PackageLoader('interssection', 'templates'),
                  extensions=['jinja2.ext.autoescape'],
                  autoescape=True)

# get template
template = env.get_template('atom.xml')


def render_as_atom(context):
    return template.render(context)
