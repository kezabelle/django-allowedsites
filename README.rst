===================
django-allowedsites
===================

Django 1.6+ library for setting your ``ALLOWED_HOSTS`` based on the domains in ``django.contrib.sites``

.. image:: https://travis-ci.org/kezabelle/django-allowedsites.svg?branch=master
  :target: https://travis-ci.org/kezabelle/django-allowedsites

Usage is something like the following, in your ``settings.py`` or equivalent::

    from allowedsites import AllowedSites
    ALLOWED_HOSTS = AllowedSites(defaults=('mytestsite.com',))
    
Or, if you want to use your cache backend::

    from allowedsites import CachedAllowedSites
    ALLOWED_HOSTS = CachedAllowedSites()
    
A single key, ``allowedsites`` will be inserted containing an unsorted collection 
of all the domains that are in the ``django.contrib.sites``. For the sake of allowing
multiple processes to keep up to date with the ``Site`` values without hitting 
the database, using a shared cache (ie: not ``LocMemCache``) is encouraged.

The ``CachedAllowedSites`` also provides an ``update_cache`` class method which
may be used as a signal listener::

    from django.db.models.signals import post_save
    from django.contrib.sites.models import Site
    post_save.connect(CachedAllowedSites.update_cache, sender=Site,
                      dispatch_uid='update_allowedsites')
    
You can modify the the defaults::

    from allowedsites import AllowedSites
    ALLOWED_HOSTS = AllowedSites(defaults=('mytestsite.com',))
    ALLOWED_HOSTS += AllowedSites(defaults=('anothersite.net',))
    ALLOWED_HOSTS -= AllowedSites(defaults=('mytestsite.com',))
    # ultimately, only anothersite.net is in the defaults

Other uses?
-----------

It *may* work with `django-csp`_ (Content Security Policy headers), 
`django-dcors`_ (Cross-Origin Resource Sharing headers) and others. I don't know.

.. _django-csp: https://github.com/mozilla/django-csp
.. _django-dcors: https://github.com/prasanthn/django-dcors
