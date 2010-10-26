#!/usr/bin/env python
# encoding: utf-8

from os.path import dirname, join, realpath


# read atom feeds (updating locals is ugly but efficient)
_current_dir = dirname(realpath(__file__))
_locals = locals()
for variable in ['atom12', 'atom23', 'atom34', 'atom_min_entry',
                 'atom_min_feed', 'atom_html']:
    filename = variable.replace('_', '-') + '.xml'
    with open(join(_current_dir, filename)) as f:
        _locals[variable] = f.read()
