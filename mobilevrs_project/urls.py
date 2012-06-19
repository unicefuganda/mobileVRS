from django.conf.urls.defaults import patterns, include, url
from ussd.urls import urlpatterns as ussd_urls


# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mobilevrs_project.views.home', name='home'),
    # url(r'^mobilevrs_project/', include('mobilevrs_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    #(r'^$', include(ussd_urls)),
)+ussd_urls

