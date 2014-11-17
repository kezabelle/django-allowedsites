# -*- coding: utf-8 -*-
from django.test import TestCase as TestCaseUsingDB


class PlaceholderTestCase(TestCaseUsingDB):
    def test_a(self):
        self.assertEqual(1, 2)
