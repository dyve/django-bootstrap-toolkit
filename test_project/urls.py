from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test_project.views.home', name='home'),
    # url(r'^test_project/', include('test_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    (r'^$', direct_to_template, {'template': 'index.html'}, "home"),
    (r'^contact$', direct_to_template, {'template': 'contact.html'}, "contact"),
    (r'^form$', 'test_bootstrap.views.test_form'),
    (r'^form_template$', 'test_bootstrap.views.test_form_with_template'),
    (r'^form_inline$', 'test_bootstrap.views.test_form_inline'),
    (r'^tabs$', 'test_bootstrap.views.test_tabs', {}, "tabs"),
)
