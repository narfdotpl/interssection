#!/usr/bin/env python
# encoding: utf-8

from feedparser import parse

from templates import render_as_atom


__all__ = ['__author__', 'Feed']
__author__ = 'Maciej Konieczny <hello@narf.pl>'


def clear_cache(method):
    """
    Clear rendered template cache.
    """

    def decorated_method(self, *args, **kwargs):
        self._xml = None
        return method(self, *args, **kwargs)

    return decorated_method


class Feed(object):

    @clear_cache
    def __init__(self, string_or_url):
        """
        Read feed from string or URL.
        """

        # accept only string (type) argument
        if not isinstance(string_or_url, basestring):
            raise TypeError('String expected, {} given.'
                            .format(string_or_url.__class__.__name__))

        # parse feed
        self._feed = parse(string_or_url)

        # raise exception if it occured during parsing
        exception = self._feed.get('bozo_exception')
        if exception:
            raise exception

    @property
    def title(self):
        return self._feed.feed.title

    @title.setter
    @clear_cache
    def title(self, new_title):
        self._feed.feed.title = new_title

    def __str__(self):
        """
        Render as Atom 1.0.
        """

        if self._xml is None:
            self._xml = render_as_atom(self._feed)
        return self._xml
