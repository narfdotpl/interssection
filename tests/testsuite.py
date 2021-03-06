#!/usr/bin/env python
# encoding: utf-8

import datetime
from uuid import uuid4

from feedparser import parse
from unittest import TestCase, main

from interssection import Feed
from tests.feeds import atom12, atom23, atom34, atom_min_entry, atom_min_feed,\
                        atom_html
from tests.server import serve_atom
from tests.validator import validate


# validate test feeds
for feed in [atom12, atom23, atom34, atom_min_entry, atom_min_feed, atom_html]:
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

    def test_raise_error_on_no_argument(self):
        with self.assertRaises(TypeError):
            Feed()

    def test_raise_error_on_incorrect_argument(self):
        for item in [0, 2.72, ('foo',), ['bar'], {'baz': 'quux'}]:
            with self.assertRaises(TypeError):
                Feed(item)

        with self.assertRaises(Exception):
            Feed('almost xml')


class TestOutput(TestCase):

    def test_print_as_valid_feed(self):
        # check minimal entry
        feed_min_entry = Feed(atom_min_entry)
        validate(str(feed_min_entry))

        # check minimal feed
        feed_min_feed = Feed(atom_min_feed)
        validate(str(feed_min_feed))

        # check result of set operation
        feed = Feed(atom12) & Feed(atom23)
        validate(str(feed))

        # check html escaping
        feed_html = Feed(atom_html)
        validate(str(feed_html))

    def test_give_unique_id_to_resultant_feed(self):
        feed12 = Feed(atom12)
        feed23 = Feed(atom23)
        id1 = parse(str(feed12 & feed23)).feed.id
        id2 = parse(str(feed12 & feed23)).feed.id
        self.assertNotEqual(id1, id2)

    def test_use_original_feed_titles_in_resultant_feed_title(self):
        feed12 = Feed(atom12)
        feed23 = Feed(atom23)
        get_title = lambda feed: parse(str(feed)).feed.title
        title = get_title(feed12 & feed23)
        title12 = get_title(feed12)
        title23 = get_title(feed23)
        self.assertIn(title12, title)
        self.assertIn(title23, title)

    def test_set_current_date_in_resultant_feed(self):
        then = datetime.datetime.utcnow().timetuple()[:6]
        feed = Feed(atom12) & Feed(atom23)
        now = datetime.datetime.utcnow().timetuple()[:6]
        parsed_time = parse(str(feed)).feed.updated_parsed[:6]
        self.assertTrue(then <= parsed_time <= now)

    def test_set_interssection_as_author_of_resultant_feed(self):
        feed = Feed(atom12) & Feed(atom23)
        parsed = parse(str(feed))
        self.assertEqual(parsed.feed.author, 'interssection')


class TestAttributes(TestCase):

    def test_expose_feed_id_as_attribute(self):
        feed = Feed(atom)
        parsed = parse(str(feed))
        self.assertEqual(feed.id, parsed.feed.id)

    def test_allow_to_change_feed_id(self):
        feed = Feed(atom)
        new_id = uuid4().urn
        feed.id = new_id
        self.assertEqual(feed.id, new_id)
        self.assertEqual(parse(str(feed)).feed.id, new_id)

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

    def setUp(self):
        self.feed12 = Feed(atom12)
        self.feed23 = Feed(atom23)
        self.feed34 = Feed(atom34)


    def test_support___and__(self):
        feed = self.feed12 & self.feed23
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 1)
        self.assertEqual(parsed.entries[0].title, '2')

        feed = self.feed12 & self.feed23 & self.feed34
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 0)

    def test_support__ge__(self):
        self.assertTrue(self.feed12 >= self.feed12)
        self.assertTrue((self.feed12 | self.feed23) >= self.feed12)
        self.assertFalse(self.feed12 >= (self.feed12 | self.feed23))

    def test_support__gt__(self):
        self.assertFalse(self.feed12 > self.feed12)
        self.assertTrue((self.feed12 | self.feed23) > self.feed12)
        self.assertFalse(self.feed12 > (self.feed12 | self.feed23))

    def test_support__le__(self):
        self.assertTrue(self.feed12 <= self.feed12)
        self.assertTrue(self.feed12 <= self.feed12 | self.feed23)
        self.assertFalse(self.feed12 <= self.feed23)

    def test_support___len__(self):
        self.assertEqual(len(self.feed12), 2)
        self.assertEqual(len(self.feed12 & self.feed23), 1)

    def test_support__lt__(self):
        self.assertFalse(self.feed12 < self.feed12)
        self.assertTrue(self.feed12 < self.feed12 | self.feed23)
        self.assertFalse(self.feed12 < self.feed23)

    def test_support___or__(self):
        feed = self.feed12 | self.feed23
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 3)
        self.assertItemsEqual([entry.title for entry in parsed.entries],
                              ['1', '2', '3'])

        feed = self.feed12 | self.feed23 | self.feed34
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 4)
        self.assertItemsEqual([entry.title for entry in parsed.entries],
                              ['1', '2', '3', '4'])

    def test_support___sub__(self):
        feed = self.feed12 - self.feed23
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 1)
        self.assertEqual(parsed.entries[0].title, '1')

        feed = self.feed23 - self.feed12 - self.feed34
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 0)

    def test_support___xor__(self):
        feed = self.feed12 ^ self.feed23
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 2)
        self.assertItemsEqual([entry.title for entry in parsed.entries],
                              ['1', '3'])

    def test_support_difference(self):
        feed = self.feed12.difference(self.feed23)
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 1)
        self.assertEqual(parsed.entries[0].title, '1')

        feed = self.feed23.difference(self.feed12, self.feed34)
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 0)

    def test_support_intersection(self):
        feed = self.feed12.intersection(self.feed23)
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 1)
        self.assertEqual(parsed.entries[0].title, '2')

        feed = self.feed12.intersection(self.feed23, self.feed34)
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 0)

    def test_support_isdisjoint(self):
        self.assertFalse(self.feed12.isdisjoint(self.feed23))
        self.assertTrue(self.feed12.isdisjoint(self.feed34))

    def test_support_issubset(self):
        self.assertTrue(self.feed12.issubset(self.feed12))
        self.assertTrue(self.feed12.issubset(self.feed12 | self.feed23))
        self.assertFalse(self.feed12.issubset(self.feed23))

    def test_support_issuperset(self):
        self.assertTrue(self.feed12.issuperset(self.feed12))
        self.assertTrue((self.feed12 | self.feed23).issuperset(self.feed12))
        self.assertFalse(self.feed12.issuperset(self.feed12 | self.feed23))

    def test_support_symmetric_difference(self):
        feed = self.feed12.symmetric_difference(self.feed23)
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 2)
        self.assertItemsEqual([entry.title for entry in parsed.entries],
                              ['1', '3'])

    def test_support_union(self):
        feed = self.feed12.union(self.feed23)
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 3)
        self.assertItemsEqual([entry.title for entry in parsed.entries],
                              ['1', '2', '3'])

        feed = self.feed12.union(self.feed23, self.feed34)
        parsed = parse(str(feed))
        self.assertEqual(len(parsed.entries), 4)
        self.assertItemsEqual([entry.title for entry in parsed.entries],
                              ['1', '2', '3', '4'])

    def test_dont_support___contains__(self):
        with self.assertRaises(TypeError):
            'foo' in Feed(atom)

    def test_dont_support_copy(self):
        with self.assertRaises(AttributeError):
            Feed(atom).copy()


class TestEntrails(TestCase):

    def test_cache_rendered_template_if_feed_wasnt_changed(self):
        feed = Feed(atom)

        str(feed)
        template1 = feed._xml

        str(feed)
        template2 = feed._xml

        self.assertIs(template1, template2)

    def test_update_template_cache_if_feed_id_was_changed(self):
        feed = Feed(atom)

        str(feed)
        template1 = feed._xml

        feed.id = uuid4().urn
        str(feed)
        template2 = feed._xml

        self.assertIsNot(template1, template2)

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
