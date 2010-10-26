#!/usr/bin/env python
# encoding: utf-8

from xml.parsers.expat import ExpatError, ParserCreate

from feedvalidator import validateString
from feedvalidator.logging import Error


class ValidationError(Exception):

    def __init__(self, event):
        self.event = event

    def __str__(self):
        # show event name
        string = self.event.__class__.__name__

        # show interesting params
        params = []
        for key in ['line', 'column', 'element', 'parent']:
            value = self.event.params.get(key)
            if value is not None:
                params.append('{} {}'.format(key, value))
        if params:
            string += ': ' + ', '.join(params)

        return string


def check_xml_wellformedness(string):
    """
    Read feed from string and raise TypeError if expat founds any errors.
    """

    if not isinstance(string, basestring):
        raise TypeError('String expected, {} given.'
                        .format(string.__class__.__name__))

    try:
        ParserCreate().Parse(string, True)
    except ExpatError:
        raise ValueError('Given string is not well-formed XML.')


def validate(string):
    """
    Read feed from string and raise ValidationError if feedvalidator founds
    any errors.
    """

    check_xml_wellformedness(string)

    for event in validateString(string)['loggedEvents']:
        if isinstance(event, Error):
            raise ValidationError(event)
