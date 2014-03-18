===================
django-allowedsites
===================

Setting your ``ALLOWED_HOSTS`` based on the domains in ``django.contrib.sites``

Usage is something like the following, in your ``settings.py`` or equivalent::

    from allowedsites import AllowedSites
    ALLOWED_HOSTS = AllowedSites(defaults=('mytestsite.com',))
    
Or, if you want to use your cache backend::

    from allowedsites import CachedAllowedSites
    ALLOWED_HOSTS = CachedAllowedSites()
    
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
