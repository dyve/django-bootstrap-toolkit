from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.views.generic import TemplateView
from demo_app.views import TemplateFormView
from demo_app.views import DemoFormView
from demo_app.views import DemoFormInlineView
from demo_app.views import DemoFormSetView
from demo_app.views import DemoTabsView
from demo_app.views import DemoPaginationView

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

    url(r'^cbv_tf$', TemplateFormView.as_view(), name='cbv_tf'),
    url(r'^cbv_df$', DemoFormView.as_view(), name='cbv_df'),
    url(r'^cbv_dfil$', DemoFormInlineView.as_view(), name='cbv_dfil'),
    url(r'^cbv_fs$', DemoFormSetView.as_view(), {}, name='cbv_fs'),
    url(r'^cbv_dt$', DemoTabsView.as_view(), {}, name='cbv_dt'),
    url(r'^cbv_dp$', DemoPaginationView.as_view(), {}, name='cbv_dp'),
)
