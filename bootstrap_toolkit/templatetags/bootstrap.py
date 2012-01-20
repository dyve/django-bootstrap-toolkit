from django.forms.widgets import CheckboxInput
from django.template import Context
from django.template.loader import get_template
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

BOOTSTRAP_DEFAULT_VERSION = '1.4.0'

BOOTSTRAP_VERSION = getattr(settings, 'BOOTSTRAP_VERSION',
    BOOTSTRAP_DEFAULT_VERSION
)

BOOTSTRAP_BASE_URL = getattr(settings, 'BOOTSTRAP_BASE_URL',
    '//twitter.github.com/bootstrap_toolkit/%s/' % BOOTSTRAP_VERSION
)

BOOTSTRAP_CSS_URL = getattr(settings, 'BOOTSTRAP_CSS_URL',
    BOOTSTRAP_BASE_URL + 'bootstrap_toolkit.min.css'
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
    # http://twitter.github.com/bootstrap_toolkit/1.3.0/bootstrap_toolkit-dropdown.js
    return BOOTSTRAP_BASE_URL + 'bootstrap_toolkit-' + name + '.js'

@register.simple_tag
def bootstrap_javascript_tag(name):
    # HTML tag to insert bootstrap_toolkit javascript file
    return u'<script src="%s"></script>' % bootstrap_javascript_url(name)

@register.simple_tag
def bootstrap_media():
    # HTML tags to insert Bootstrap stylesheet and javascript
    return bootstrap_media()

@register.filter
def as_bootstrap(form):
    # Filter to Bootstrap a Django form, analogous to as_p, as_table, as_ul
    return get_template("bootstrap_toolkit/form.html").render(
        Context({
            'form': form
        })
    )

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

@register.filter
def input_type(field):
    widget = field.field.widget
    bootstrap_input_type = getattr(widget.attrs, 'bootstrap_input_type', None)
    if bootstrap_input_type:
        return bootstrap_input_type
    if isinstance(widget, CheckboxInput):
        return u'checkbox'
    return u'default'

@register.simple_tag
def active_url(request, url, output=u'active'):
    # Tag that outputs text if the given url is active for the request
    if url == request.path:
        return output
    return ''

@register.filter
def as_bootstrap_choices(html_ul):
    # Nasty hack to make widgets with choices behave
    return mark_safe(str(html_ul).replace('<ul>', '<ul class="inputs-list">'))

@register.filter
def pagination(page, range=5):
    # Filter to generate Bootstrap pagination from a page
    num_pages = page.paginator.num_pages
    current_page = page.number
    range_min = max(current_page - range, 1)
    range_max = min(current_page + range, num_pages)
    return get_template("bootstrap_toolkit/pagination.html").render(
        Context({
            'page': page,
            'num_pages': num_pages,
            'current_page': current_page,
            'range_min': range_min,
            'range_max': range_max,
        })
    )