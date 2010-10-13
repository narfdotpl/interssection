#!/usr/bin/env python
# encoding: utf-8

from feedparser import parse
from unittest import TestCase, main

from interssection import Feed
from tests.feeds import atom12, atom23, atom34
from tests.server import serve_atom
from tests.validator import validate


__author__ = 'Maciej Konieczny <hello@narf.pl>'


# validate test feeds
for feed in [atom12, atom23, atom34]:
    validate(feed)

# create handy alias
atom = atom12


class TestInput(TestCase):

    def assert_content_is_the_same(self, old, new):
        old = parse(old)
        new = parse(new)

        # check meta info
        for attr_name in ['title', 'id', 'updated']:
            self.assertEqual(getattr(old.feed, attr_name),
                             getattr(new.feed, attr_name))

        # check number of entries
        self.assertEqual(len(old.entries), len(new.entries))

        # check invidual entries
        sort_key = lambda entry: entry.id
        old.entries.sort(key=sort_key)
        new.entries.sort(key=sort_key)
        for old_entry, new_entry in zip(old.entries, new.entries):
            for attr_name in ['title', 'id', 'updated', 'summary']:
                self.assertEqual(getattr(old_entry, attr_name),
                                 getattr(new_entry, attr_name))


    def test_read_feed_from_string(self):
        xml = str(Feed(atom))
        self.assert_content_is_the_same(atom, xml)

    def test_read_feed_from_url(self):
        host = 'localhost'
        port = 8000
        url = 'http://{}:{}/'.format(host, port)

        serve_atom(host, port, atom)
        xml = str(Feed(url))
        self.assert_content_is_the_same(atom, xml)

    def test_raise_error_on_incorrect_argument(self):
        for item in [0, 2.72, ('foo',), ['bar'], {'baz': 'quak'}]:
            with self.assertRaises(TypeError):
                Feed(item)

        with self.assertRaises(Exception):
            Feed('almost xml')


class TestOutput(TestCase):

    def test_print_as_valid_feed(self):
        xml = str(Feed(atom))
        validate(xml)

    def test_give_unique_id_to_resultant_feed(self):
        self.fail()

    def test_set_current_date_in_resultant_feed(self):
        self.fail()

    def test_set_interssection_as_author_of_resultant_feed(self):
        self.fail()


class TestAttributes(TestCase):

    def test_expose_feed_title_as_attribute(self):
        feed = Feed(atom)
        parsed = parse(str(feed))
        self.assertEqual(feed.title, parsed.feed.title)

    def test_allow_to_change_feed_title(self):
        feed = Feed(atom)
        new_title = feed.title + 'foo'
        feed.title = new_title
        self.assertEqual(feed.title, new_title)
        self.assertEqual(parse(str(feed)).feed.title, new_title)


class TestSetOperations(TestCase):

    def test_support_x(self):
        self.fail()

    def test_dont_support_y(self):
        self.fail()


class TestEntrails(TestCase):

    def test_cache_rendered_template_if_feed_wasnt_changed(self):
        feed = Feed(atom)

        str(feed)
        template1 = feed._xml

        str(feed)
        template2 = feed._xml

        self.assertIs(template1, template2)

    def test_update_template_cache_if_feed_title_was_changed(self):
        feed = Feed(atom)

        str(feed)
        template1 = feed._xml

        feed.title += 'foo'
        str(feed)
        template2 = feed._xml

        self.assertIsNot(template1, template2)


if __name__ == '__main__':
    main()
