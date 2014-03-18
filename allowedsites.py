# -*- coding: utf-8 -*-

class Sites(object):
    """
    Sites are unordered, because seriously who cares.
    """
    
    __slots__ = ('defaults', 'sites')
    
    def __init__(self, defaults=None):
        if defaults is None:
            defaults = ()
        self.defaults = frozenset(defaults)
        self.sites = None
        
    def get_raw_sites(self):
        from django.contrib.sites.models import Site
        return Site.objects.all().iterator()
        
    def get_sites(self):
        raw_sites = self.get_raw_sites()
        return frozenset(site.domain for site in raw_sites)
        
    def get_merged_allowed_hosts(self):
        sites = self.get_sites()
        return self.defaults.union(sites)
        
    def __iter__(self):
        return iter(self.get_merged_allowed_hosts())
        
    def __str__(self):
        return ', '.join(self.get_merged_allowed_hosts())
        
    def __contains__(self, other):
        return other in self.get_merged_allowed_hosts()
    
    def __len__(self):
        return len(self.get_merged_allowed_hosts())
        
    def __add__(self, other):
        more_defaults = self.defaults.union(other.defaults)
        return self.__class__(defaults=more_defaults)
        
    def __sub__(self, other):
        less_defaults = self.defaults.difference(other.defaults)
        return self.__class__(defaults=less_defaults)

class AllowedSites(Sites):
    """
    This only exists to allow isinstance to differentiate between
    the various Site subclasses
    """
    __slots__ = ('defaults', 'sites')
    pass


class CachedAllowedSites(Sites):
    """
    Sets the given ``Site`` domains into the ``default`` cache.
    Expects the cache to be shared between processes, such that
    a signal listening for ``Site`` creates will be able to add to
    the cache's contents for other processes to pick up on.
    """
    __slots__ = ('defaults', 'sites', 'key')
    
    def __init__(self, defaults=None, key='allowedsites'):
        super(CachedAllowedSites, self).__init__(defaults=defaults)
        self.key = key
    
    def get_cached_sites(self):
        from django.core.cache import cache
        results = cache.get(self.key)
        return results

    def get_sites(self):
        cached = self.get_cached_sites()
        if cached is None:
            cached = super(CachedAllowedSites, self).get_sites()
            cache.set(self.key, cached)
        return cached
    
    def get_merged_allowed_hosts(self):
        sites = self.get_sites()
        return self.defaults.union(sites)
