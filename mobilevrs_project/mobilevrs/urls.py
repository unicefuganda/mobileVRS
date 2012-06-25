from django.conf.urls.defaults import patterns, include, url
from ussd.urls import urlpatterns as ussd_urls
from mobilevrs.views import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'/$', ussd_menu),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    #(r'^$', include(ussd_urls)),
)
