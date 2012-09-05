from django.forms import BaseForm
from django.forms.forms import BoundField
from django.forms.widgets import TextInput, CheckboxInput, CheckboxSelectMultiple, RadioSelect
from django.template import Context
from django.template.loader import get_template
from django import template
from django.conf import settings

BOOTSTRAP_BASE_URL = getattr(settings, 'BOOTSTRAP_BASE_URL',
    'http://twitter.github.com/bootstrap/assets/'
)

BOOTSTRAP_JS_BASE_URL = getattr(settings, 'BOOTSTRAP_JS_BASE_URL',
    BOOTSTRAP_BASE_URL + 'js/'
)

BOOTSTRAP_JS_URL = getattr(settings, 'BOOTSTRAP_JS_URL',
    None
)

BOOTSTRAP_CSS_BASE_URL = getattr(settings, 'BOOTSTRAP_CSS_BASE_URL',
    BOOTSTRAP_BASE_URL + 'css/'
)

BOOTSTRAP_CSS_URL = getattr(settings, 'BOOTSTRAP_CSS_URL',
    BOOTSTRAP_CSS_BASE_URL + 'bootstrap.css'
)

register = template.Library()

@register.simple_tag
def bootstrap_stylesheet_url():
    """
    URL to Bootstrap Stylesheet (CSS)
    """
    return BOOTSTRAP_CSS_URL

@register.simple_tag
def bootstrap_stylesheet_tag():
    """
    HTML tag to insert Bootstrap stylesheet
    """
    return u'<link rel="stylesheet" href="%s">' % bootstrap_stylesheet_url()

@register.simple_tag
def bootstrap_javascript_url(name):
    """
    URL to Bootstrap javascript file
    """
    if BOOTSTRAP_JS_URL:
        return BOOTSTRAP_JS_URL
    return BOOTSTRAP_JS_BASE_URL + 'bootstrap-' + name + '.js'


@register.simple_tag
def bootstrap_javascript_tag(name):
    """
    HTML tag to insert bootstrap_toolkit javascript file
    """

    return u'<script src="%s"></script>' % bootstrap_javascript_url(name)

@register.filter
def as_bootstrap(form_or_field, layout='vertical,false'):
    """
    Render a field or a form according to Bootstrap guidelines
    """
    params = split(layout, ",")
    layout = str(params[0]).lower()

    if len(params) > 1:
        float = str(params[1]).lower() == "float"

    if isinstance(form_or_field, BaseForm):
        return get_template("bootstrap_toolkit/form.html").render(
            Context({
                'form': form_or_field,
                'layout': layout,
                'float': float,
            })
        )
    elif isinstance(form_or_field, BoundField):
        return get_template("bootstrap_toolkit/field.html").render(
            Context({
                'field': form_or_field,
                'layout': layout,
                'float': float,
            })
        )
    else:
        # Display the default
        return settings.TEMPLATE_STRING_IF_INVALID

@register.filter
def is_disabled(field):
    """
    Returns True if fields is disabled, readonly or not marked as editable, False otherwise
    """
    if not getattr(field.field, 'editable', True):
        return True
    if getattr(field.field.widget.attrs, 'readonly', False):
        return True
    if getattr(field.field.widget.attrs, 'disabled', False):
        return True
    return False

@register.filter
def is_enabled(field):
    """
    Shortcut to return the logical negative of is_disabled
    """
    return not is_disabled(field)

@register.filter
def bootstrap_input_type(field):
    """
    Return input type to use for field
    """
    try:
        widget = field.field.widget
    except:
        raise ValueError("Expected a Field, got a %s" % type(field))
    input_type = getattr(widget.attrs, 'bootstrap_input_type', None)
    if input_type:
        return input_type
    if isinstance(widget, TextInput):
        return u'text'
    if isinstance(widget, CheckboxInput):
        return u'checkbox'
    if isinstance(widget, CheckboxSelectMultiple):
        return u'multicheckbox'
    if isinstance(widget, RadioSelect):
        return u'radioset'
    return u'default'

@register.simple_tag
def active_url(request, url, output=u'active'):
    # Tag that outputs text if the given url is active for the request
    if url == request.path:
        return output
    return ''

@register.filter
def pagination(page, range=5):
    """
    Generate Bootstrap pagination links from a page object
    """
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

@register.filter
def split(str, splitter):
    """
    Split a string
    """
    return str.split(splitter)
