from django.forms.widgets import CheckboxInput
from django.template import Context
from django.template.loader import get_template
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

BOOTSTRAP_DEFAULT_VERSION = '1.4.0'

BOOTSTRAP_VERSION =  getattr(settings, 'BOOTSTRAP_VERSION',
    BOOTSTRAP_DEFAULT_VERSION
)

BOOTSTRAP_BASE_URL = getattr(settings, 'BOOTSTRAP_BASE_URL',
    '//twitter.github.com/bootstrap/%s/' % BOOTSTRAP_VERSION
)

BOOTSTRAP_CSS_URL = getattr(settings, 'BOOTSTRAP_CSS_URL',
    BOOTSTRAP_BASE_URL + 'bootstrap.min.css'
)

register = template.Library()

@register.simple_tag
def bootstrap_stylesheet_url():
    # URL to Bootstrap Stylesheet (CSS file)
   return BOOTSTRAP_CSS_URL

@register.simple_tag
def bootstrap_stylesheet_tag():
    # HTML tag to insert Bootstrap stylesheet
    return u'<link rel="stylesheet" href="%s">' % bootstrap_stylesheet_url()

@register.simple_tag
def bootstrap_javascript_url(name):
    # URL to Bootstrap javascript file
    # http://twitter.github.com/bootstrap/1.3.0/bootstrap-dropdown.js
    return BOOTSTRAP_BASE_URL + 'bootstrap-' + name + '.js'

@register.simple_tag
def bootstrap_javascript_tag(name):
    # HTML tag to insert bootstrap javascript file
    return u'<script src="%s"></script>' % bootstrap_javascript_url(name)

@register.simple_tag
def bootstrap_media():
    # HTML tags to insert Bootstrap stylesheet and javascript
    return bootstrap_media()


@register.filter
def bootstrap(form):
    output = []
    output.append(unicode(form.non_field_errors()))

    for field in form.visible_fields():

        output.append(u'<div class="clearfix%s%s">'%(' error' if field.errors else '',
                                                     ' required' if field.field.required else ''))

        disabled = u' disabled' if is_disabled(field) else ''
        if isinstance(field.field.widget, CheckboxInput):  # checkbox
            output.append(u'<div class="input">\n<ul class="inputs-list">\n<li>')
            output.append(u'<label class="%s">'%disabled)
            output.append(unicode(field))
            output.append(u'<span>%s</span>'%field.label)
            output.append(u'</label>\n</li>\n</ul>')

        elif hasattr(field.field.widget, 'choices'):  # choices
            output.append('<label>%s</label>'%field.label)
            output.append('<div class="input%s">'%disabled)
            output.append(unicode(field).replace('<ul>', '<ul class="inputs-list">'))

        else:  #default
            output.append(field.label_tag())
            output.append(u'<div class="input%s">'%disabled)
            output.append(unicode(field))

        for error in field.errors:
            output.append(u'<span class="help-inline">%s</span>'%error)

        if field.help_text:
            output.append(u'<span class="help-block">%s</span>'%field.help_text)

        output.append(u'</div> <!-- input -->')
        output.append(u'</div> <!-- clearfix -->')

    for field in form.hidden_fields():
        output.append(field)

    return mark_safe('\n'.join(output))


@register.filter
def is_disabled(field):
    # Filter to determine if a field is disabled
    if not getattr(field.field, 'editable', True):
        return True
    if getattr(field.field.widget.attrs, 'readonly', False):
        return True
    if getattr(field.field.widget.attrs, 'disabled', False):
        return True
    return False


@register.filter
def is_enabled(field):
    # Filter to determine if a field is enabled
    return not is_disabled(field)


@register.simple_tag
def active_url(request, url, output=u'active'):
    # Tag that outputs text if the given url is active for the request
    if url == request.path:
        return output
    return ''
