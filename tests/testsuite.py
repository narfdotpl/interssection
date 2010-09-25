#!/usr/bin/env python
# encoding: utf-8

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

    def test_read_feed_from_string(self):
        self.assertEqual(str(Feed(atom)), atom)

    def test_read_feed_from_url(self):
        host = 'localhost'
        port = 8000
        url = 'http://{}:{}/'.format(host, port)

        serve_atom(host, port, atom)
        self.assertEqual(str(Feed(url)), atom)

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


class TestOptions(TestCase):

    def test_allow_to_set_title(self):
        self.fail()


class TestSetOperations(TestCase):

    def test_support_x(self):
        self.fail()

    def test_dont_support_y(self):
        self.fail()


if __name__ == '__main__':
    main()
