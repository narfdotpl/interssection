#!/usr/bin/env python
# encoding: utf-8

from os.path import dirname, join, realpath

from jinja2 import Template


__all__ = ['render_as_atom']


# create template
with open(join(dirname(realpath(__file__)), 'atom.xml')) as f:
    template = Template(f.read())


def render_as_atom(context):
    return template.render(context)
