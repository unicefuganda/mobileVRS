from django.conf.urls.defaults import patterns, include, url
from ussd.urls import urlpatterns as ussd_urls
from mobilevrs.urls import urlpatterns as vrs_urls
from django.views.generic.simple import direct_to_template


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
#    url(r'ussd/$', include('mobilevrs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^account/', include('rapidsms.urls.login_logout')),
    url(r'^$', direct_to_template, {'template':'ussd/yo.txt'}, name='rapidsms-dashboard'),
    url('^accounts/login', 'rapidsms.views.login'),
    url('^accounts/logout', 'rapidsms.views.logout'),
)+vrs_urls
