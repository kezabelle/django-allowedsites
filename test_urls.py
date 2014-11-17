# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^admin_mountpoint/', include(admin.site.urls)),
)
