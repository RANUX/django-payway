from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'payway_demo.views.home', name='home'),
    # url(r'^payway_demo/', include('payway_demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('payway.accounts.urls')),
    (r'^webmoney/', include('payway.webmoney.urls')),
    (r'^qiwi/', include('payway.qiwi.urls')),
    (r'^orders/', include('payway.orders.urls')),
    (r'^merchants/', include('payway.merchants.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
)
