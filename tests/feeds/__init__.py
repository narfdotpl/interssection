#!/usr/bin/env python
# encoding: utf-8

from os.path import dirname, join, realpath


# read atom feeds
_current_dir = dirname(realpath(__file__))

with open(join(_current_dir, 'atom12.xml')) as f:
    atom12 = f.read()

with open(join(_current_dir, 'atom23.xml')) as f:
    atom23 = f.read()

with open(join(_current_dir, 'atom34.xml')) as f:
    atom34 = f.read()

with open(join(_current_dir, 'atom-min-entry.xml')) as f:
    atom_min_entry = f.read()

with open(join(_current_dir, 'atom-min-feed.xml')) as f:
    atom_min_feed = f.read()

with open(join(_current_dir, 'atom-html.xml')) as f:
    atom_html = f.read()
