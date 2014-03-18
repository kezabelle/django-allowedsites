
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
        self.sites = frozenset(site.domain for site in sites)
        return self.defaults.union(self.sites)
        
    def __iter__(self):
        return iter(self.get_sites())
        
    def __str__(self):
        return ', '.join(self.get_sites())
        
    def __contains__(self, other):
        return other in self.get_sites()
    
    def __len__(self):
        return len(self.get_sites())
        
    def __add__(self, other):
        more_defaults = self.defaults.union(other.defaults)
        return self.__class__(defaults=more_defaults)

class AllowedSites(Sites):
    """
    This only exists to allow isinstance to differentiate between
    the various Site subclasses
    """
    __slots__ = ('defaults', 'sites')
    pass


class CachedAllowedSites(Sites):
    __slots__ = ('defaults', 'sites')
    pass

