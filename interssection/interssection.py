#!/usr/bin/env python
# encoding: utf-8

import datetime
import uuid

from feedparser import parse

from templates import render_as_atom


__all__ = ['__author__', 'Feed']
__author__ = 'Maciej Konieczny <hello@narf.pl>'


class MetaFeed(type):

    def __new__(cls, class_name, base_classes, attributes_dict):
        for method_name in ['__and__', '__ge__', '__gt__', '__le__', '__len__',
                            '__lt__', '__or__', '__sub__', '__xor__',
                            'difference', 'intersection', 'isdisjoint',
                            'issubset', 'issuperset', 'symmetric_difference',
                            'union']:
            if method_name not in attributes_dict:
                method = create_set_method(method_name)
                attributes_dict[method_name] = method

        return type.__new__(cls, class_name, base_classes, attributes_dict)


def clear_cache(method):
    """
    Clear rendered template cache.
    """

    def decorated_method(self, *args, **kwargs):
        self._xml = None
        return method(self, *args, **kwargs)

    return decorated_method


def create_set_method(method_name):
    def method(*feeds):
        # prepare feeds
        for feed in feeds:
            if feed._entry_ids is None:
                feed._entries_by_id = dict((e.id, e) for e in feed._entries)
                feed._entry_ids = frozenset(feed._entries_by_id.iterkeys())

        # get id sets
        first_set = feeds[0]._entry_ids
        other_sets = (feed._entry_ids for feed in feeds[1:])

        # run method
        result = getattr(first_set, method_name)(*other_sets)

        # return bools, etc.
        if not isinstance(result, frozenset):
            return result

        # create resultant feed
        entries_by_id = {}
        for feed in feeds:
            entries_by_id.update(feed._entries_by_id)
        entries = [entries_by_id[id] for id in result]

        title = (' ' + method_name + ' ').join(feed.title for feed in feeds)
        return Feed(id=get_urn(), title=title, updated=get_iso8601_datetime(),
                    author='interssection', entries=entries)

    return method


class Feed(object):

    __metaclass__ = MetaFeed

    @clear_cache
    def __init__(self, string_or_url=None, **feed_attributes):
        """
        Read feed from string or URL.
        """

        # set initial...
        self._entry_ids = None

        # pretend it's `def __init__(self, string_or_url):`
        if string_or_url is None:
            if not feed_attributes:
                message = '__init__() takes exactly 2 arguments (1 given)'
                raise TypeError(message)

            # use backdoor
            for name in ['id', 'title', 'updated', 'author', 'entries']:
                setattr(self, '_' + name, feed_attributes[name])
            return

        # accept only string (type) argument
        if not isinstance(string_or_url, basestring):
            raise TypeError('String expected, {} given.'
                            .format(string_or_url.__class__.__name__))

        # parse feed
        parsed = parse(string_or_url)

        # raise exception if it occured during parsing
        exception = parsed.get('bozo_exception')
        if exception:
            raise exception

        # set attributes
        for name in ['id', 'title', 'updated', 'author']:
            setattr(self, '_' + name, parsed.feed.get(name))
        self._entries = parsed.entries

    @property
    def title(self):
        return self._title

    @title.setter
    @clear_cache
    def title(self, new_title):
        self._title = new_title

    def __str__(self):
        """
        Render as Atom 1.0.
        """

        if self._xml is None:
            # pick feed attributes
            context = {'entries': self._entries}
            for name in ['id', 'title', 'updated', 'author']:
                context[name] = getattr(self, '_' + name)

            self._xml = render_as_atom(context)

        return self._xml


def get_iso8601_datetime():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def get_urn():
    return uuid.uuid4().urn
