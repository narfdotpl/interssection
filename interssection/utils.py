#!/usr/bin/env python
# encoding: utf-8

import datetime
import uuid


def get_iso8601_datetime():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


def get_urn():
    return uuid.uuid4().urn
