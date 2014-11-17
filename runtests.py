#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from django.conf import settings
import django


def get_settings():
    import test_settings
    setting_attrs = {}
    for attr in dir(test_settings):
        if attr.isupper():
            setting_attrs[attr] = getattr(test_settings, attr)
    return setting_attrs


def runtests():
    if not settings.configured:
        settings.configure(**get_settings())

    # Compatibility with Django 1.7's stricter initialization
    if hasattr(django, 'setup'):
        django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    from django.test.runner import DiscoverRunner as Runner
    # reminder to self: an ImportError in the tests may either turn up
    # or may cause this thing to barf with this crap:
    # AttributeError: 'module' object has no attribute 'tests'
    test_args = ['.']
    failures = Runner(
        verbosity=2, interactive=True, failfast=False).run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
