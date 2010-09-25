#!/usr/bin/env python
# encoding: utf-8

import feedparser


__all__ = ['__author__', 'Feed']
__author__ = 'Maciej Konieczny <hello@narf.pl>'


class Feed(object):

    def __init__(self, string_or_url):
        """
        Read feed from string or URL.
        """

        # accept only string (type) argument
        if not isinstance(string_or_url, basestring):
            raise TypeError('String expected, {} given.'
                            .format(string_or_url.__class__.__name__))

        # parse feed
        self._feed = feedparser.parse(string_or_url)

        # raise exception if it occured during parsing
        exception = self._feed.get('bozo_exception')
        if exception:
            raise exception

    def __str__(self):
        return str(self._feed)
