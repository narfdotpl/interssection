#!/usr/bin/env python
# encoding: utf-8
"""
Core module providing Feed class.
"""

from feedparser import parse

from interssection.templates import render_as_atom
from interssection.utils import get_iso8601_datetime, get_urn


__all__ = ['__author__', '__version__', 'Feed']
__author__ = 'Maciej Konieczny <hello@narf.pl>'
__version__ = '0.1.0'


class MetaFeed(type):
    """
    Metaclass that adds methods to support set operations on feeds.

    All frozenset methods are added apart from `copy()` and
    `__contains__(elem)`.
    """

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
    """
    Return method that accepts Feed instances as arguments and calls method
    of given name on arguments' private frozenset attributes to produce
    return value.
    """

    def method(*feeds):
        # prepare feeds (they're lazy)
        for feed in feeds:
            if feed._entry_ids is None:
                feed._entries_by_id = dict((e.id, e) for e in feed._entries)
                feed._entry_ids = frozenset(feed._entries_by_id.iterkeys())

        # get id sets
        first_set = feeds[0]._entry_ids
        other_sets = (feed._entry_ids for feed in feeds[1:])

        # run method on id sets
        result = getattr(first_set, method_name)(*other_sets)

        # return bools and ints
        if not isinstance(result, frozenset):
            return result

        # gather entries for new feed
        entries_by_id = {}
        for feed in feeds:
            entries_by_id.update(feed._entries_by_id)
        entries = [entries_by_id[id] for id in result]

        # set feed title
        title = (' ' + method_name + ' ').join(feed.title for feed in feeds)

        # return new feed
        return Feed(id=get_urn(), title=title, updated=get_iso8601_datetime(),
                    author='interssection', entries=entries)

    return method


class Feed(object):
    """
    Class that reads Atom and RSS feeds and lets you treat them like sets.

    Feed objects have to be instantiated with single string argument that
    can be either feed URL or raw XML.

    Feed instances have two attributes: `id` and `title`, and support all
    frozenset methods apart from `copy()` and `__contains__(elem)`.
    """

    __metaclass__ = MetaFeed

    @clear_cache
    def __init__(self, string_or_url=None, **feed_attributes):
        """
        Read feed from string or URL.
        """

        # book place for ids frozenset (don't generate it now, be lazy)
        self._entry_ids = None

        # pretend it's `def __init__(self, string_or_url):`
        if string_or_url is None:
            if not feed_attributes:
                message = '__init__() takes exactly 2 arguments (1 given)'
                raise TypeError(message)

            # use backdoor to set attributes without parsing any string
            for name in ['id', 'title', 'updated', 'author', 'entries']:
                setattr(self, '_' + name, feed_attributes[name])
            return

        # accept only string argument (url is also of string type)
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
    def id(self):
        return self._id

    @id.setter
    @clear_cache
    def id(self, new_id):
        self._id = new_id

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

        # cache rendered template
        if self._xml is None:
            # context = {'id': self._id, ...}
            context = dict((name, getattr(self, '_' + name)) for name in
                           ['id', 'title', 'updated', 'author', 'entries'])
            self._xml = render_as_atom(context)

        return self._xml
