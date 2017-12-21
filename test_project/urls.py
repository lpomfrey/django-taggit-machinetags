# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django
from pkg_resources import parse_version

if parse_version(django.__version__) >= parse_version('2.0.0'):
    from django.urls import include, path
else:
    from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # path('', 'test_project.views.home', name='home'),
    # path('test_project/', include('test_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # path('admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # path('admin/', include(admin.site.urls)),
]
