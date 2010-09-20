#!/usr/bin/env python
# encoding: utf-8

from unittest import TestCase, main

from interssection import Feed


__author__ = 'Maciej Konieczny <hello@narf.pl>'


class TestInput(TestCase):

    def test_read_feed_from_string(self):
        self.fail()

    def test_read_feed_from_url(self):
        self.fail()


class TestOutput(TestCase):

    def test_print_as_valid_feed(self):
        self.fail()

    def test_print_entries_sorted_by_date(self):
        self.fail()

    def test_dont_change_meta_info_in_source_feed(self):
        self.fail()

    def test_give_unique_id_to_resultant_feed(self):
        self.fail()

    def test_set_current_date_in_resultant_feed(self):
        self.fail()

    def test_set_interssection_as_author_of_resultant_feed(self):
        self.fail()


class TestOptions(TestCase):

    def test_allow_to_change_title(self):
        self.fail()


class TestSetOperations(TestCase):

    def test_support_x(self):
        self.fail()

    def test_dont_support_y(self):
        self.fail()


if __name__ == '__main__':
    main()
