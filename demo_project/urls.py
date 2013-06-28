from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demo_project.views.home', name='home'),
    # url(r'^demo_project/', include('demo_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    url(r'^contact$', TemplateView.as_view(template_name='contact.html'), name="contact"),
    url(r'^form$', 'demo_app.views.demo_form'),
    url(r'^form_template$', 'demo_app.views.demo_form_with_template'),
    url(r'^form_inline$', 'demo_app.views.demo_form_inline'),
    url(r'^formset$', 'demo_app.views.demo_formset', {}, "formset"),
    url(r'^tabs$', 'demo_app.views.demo_tabs', {}, "tabs"),
    url(r'^pagination$', 'demo_app.views.demo_pagination', {}, "pagination"),
    url(r'^widgets$', 'demo_app.views.demo_widgets', {}, "widgets"),
    url(r'^buttons$', TemplateView.as_view(template_name='buttons.html'), name="buttons"),
)
