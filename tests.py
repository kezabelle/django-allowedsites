# -*- coding: utf-8 -*-
from allowedsites import AllowedSites
from django.contrib.sites.models import Site
from django.http.request import validate_host
from django.test import TestCase as TestCaseUsingDB


class AllowedSitesTestCase(TestCaseUsingDB):
    def setUp(self):
        Site.objects.all().delete()  # remove default
        Site.objects.create(domain='example.com:8080', name='test')
        Site.objects.create(domain='example.org:8181', name='test 2')

    def test_get_raw_sites_unevaluated(self):
        allowed_cls = AllowedSites(defaults=['yay.com'])
        with self.assertNumQueries(0):
            allowed_cls.get_raw_sites()

    def test_get_raw_sites_evaluated(self):
        allowed_cls = AllowedSites(defaults=['yay.com'])
        with self.assertNumQueries(1):
            data = tuple(allowed_cls.get_raw_sites())
            self.assertEqual(len(data), 2)
        # do it again to demonstrate it uses iterator()
        with self.assertNumQueries(1):
            data = tuple(allowed_cls.get_raw_sites())
            self.assertEqual(len(data), 2)

    def test_get_domains(self):
        allowed_cls = AllowedSites(defaults=['yay.com'])
        with self.assertNumQueries(1):
            data = allowed_cls.get_domains()
            self.assertEqual(data, frozenset(['example.com', 'example.org']))

    def test_iterable(self):
        """
        this is what Django does internally in django.http.request
        allowed_cls is synonymous with settings.ALLOWED_HOSTS
        """
        allowed_cls = AllowedSites(defaults=['yay.com'])
        with self.assertNumQueries(1):
            self.assertTrue(validate_host('example.com', allowed_cls))
        with self.assertNumQueries(1):
            self.assertTrue(validate_host('example.org', allowed_cls))
        with self.assertNumQueries(1):
            self.assertFalse(validate_host('djangoproject.com', allowed_cls))
        # ideally this should be 0 queries, because it's a default ...
        with self.assertNumQueries(1):
            self.assertTrue(validate_host('yay.com', allowed_cls))

    def test_length(self):
        allowed_cls = AllowedSites(defaults=['yay.com'])
        self.assertEqual(len(allowed_cls), 3)

    def test_containment(self):
        allowed_cls = AllowedSites(defaults=['yay.com'])
        self.assertIn('example.org', allowed_cls)
        self.assertNotIn('djangoproject.org', allowed_cls)

    def test_bool_true(self):
        allowed_cls = AllowedSites()
        self.assertTrue(allowed_cls)

    def test_bool_false(self):
        allowed_cls = AllowedSites()
        Site.objects.all().delete()
        self.assertFalse(allowed_cls)

    def test_equality(self):
        allowed_cls = AllowedSites()
        allowed_cls2 = AllowedSites()
        self.assertEqual(allowed_cls, allowed_cls2)

    def test_inequality(self):
        allowed_cls = AllowedSites()
        allowed_cls2 = AllowedSites(defaults='test.com')
        self.assertNotEqual(allowed_cls, allowed_cls2)
