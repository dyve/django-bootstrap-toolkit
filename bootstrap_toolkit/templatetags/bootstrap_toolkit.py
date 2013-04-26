import re

from math import floor

from django.forms import BaseForm
from django.forms.forms import BoundField
from django.forms.widgets import TextInput, CheckboxInput, CheckboxSelectMultiple, RadioSelect
from django.template import Context
from django.template.loader import get_template
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.html import escape


BOOTSTRAP_BASE_URL = getattr(settings, 'BOOTSTRAP_BASE_URL',
                             'http://twitter.github.io/bootstrap/assets/'
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
def bootstrap_stylesheet_url(css=None):
    """
    URL to Bootstrap Stylesheet (CSS)
    """
    url = BOOTSTRAP_CSS_URL
    if css:
        url = BOOTSTRAP_CSS_BASE_URL + u'bootstrap-%s.css' % css
    else:
        url = BOOTSTRAP_CSS_URL
    return url


@register.simple_tag
def bootstrap_stylesheet_tag(css=None):
    """
    HTML tag to insert Bootstrap stylesheet
    """
    return u'<link rel="stylesheet" href="%s">' % bootstrap_stylesheet_url(css)


@register.simple_tag
def bootstrap_javascript_url(name=None):
    """
    URL to Bootstrap javascript file
    """
    if BOOTSTRAP_JS_URL:
        return BOOTSTRAP_JS_URL
    if name:
        return BOOTSTRAP_JS_BASE_URL + 'bootstrap-' + name + '.js'
    else:
        return BOOTSTRAP_JS_BASE_URL + 'bootstrap.min.js'


@register.simple_tag
def bootstrap_javascript_tag(name=None):
    """
    HTML tag to insert bootstrap_toolkit javascript file
    """
    url = bootstrap_javascript_url(name)
    if url:
        return u'<script src="%s"></script>' % url
    return u''


@register.filter
def as_bootstrap(form_or_field, layout='vertical,false'):
    """
    Render a field or a form according to Bootstrap guidelines
    """
    params = split(layout, ",")
    layout = str(params[0]).lower()

    try:
        float = str(params[1]).lower() == "float"
    except IndexError:
        float = False

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
    input_type = getattr(widget, 'bootstrap_input_type', None)
    if input_type:
        return unicode(input_type)
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
def pagination(page, pages_to_show=11):
    """
    Generate Bootstrap pagination links from a page object
    """
    context = get_pagination_context(page, pages_to_show)
    return get_template("bootstrap_toolkit/pagination.html").render(Context(context))


@register.filter
def split(text, splitter):
    """
    Split a string
    """
    return text.split(splitter)


@register.filter
def html_attrs(attrs):
    """
    Display the attributes given as html attributes :
    >>> import collections
    >>> html_attrs(collections.OrderedDict([('href',"http://theurl.com/img.png"), ('alt','hi "guy')]))
    u'href="http://theurl.com/img.png" alt="hi &quot;guy" '
    """
    pairs = []
    for name, value in attrs.items():
        pairs.append(u'%s="%s"' % (escape(name), escape(value)))
    return mark_safe(u' '.join(pairs))


@register.simple_tag(takes_context=True)
def bootstrap_messages(context, *args, **kwargs):
    """
    Show request messages in Bootstrap style
    """
    return get_template("bootstrap_toolkit/messages.html").render(context)


@register.inclusion_tag("bootstrap_toolkit/form.html")
def bootstrap_form(form, **kwargs):
    """
    Render a form
    """
    context = kwargs.copy()
    context['form'] = form
    return context


@register.inclusion_tag("bootstrap_toolkit/formset.html")
def bootstrap_formset(formset, **kwargs):
    """
    Render a formset
    """
    context = kwargs.copy()
    context['formset'] = formset
    return context


@register.inclusion_tag("bootstrap_toolkit/field.html")
def bootstrap_field(field, **kwargs):
    """
    Render a field
    """
    context = kwargs.copy()
    context['field'] = field
    return context


@register.inclusion_tag("bootstrap_toolkit/pagination.html")
def bootstrap_pagination(page, **kwargs):
    """
    Render pagination for a page
    """
    pagination_kwargs = kwargs.copy()
    pagination_kwargs['page'] = page
    return get_pagination_context(**pagination_kwargs)


def get_pagination_context(page, pages_to_show=11, url=None, extra=None):
    """
    Generate Bootstrap pagination context from a page object
    """
    pages_to_show = int(pages_to_show)
    if pages_to_show < 1:
        raise ValueError("Pagination pages_to_show should be a positive integer, you specified %s" % pages_to_show)
    num_pages = page.paginator.num_pages
    current_page = page.number
    half_page_num = int(floor(pages_to_show / 2)) - 1
    if half_page_num < 0:
        half_page_num = 0
    first_page = current_page - half_page_num
    if first_page <= 1:
        first_page = 1
    if first_page > 1:
        pages_back = first_page - half_page_num
        if pages_back < 1:
            pages_back = 1
    else:
        pages_back = None
    last_page = first_page + pages_to_show - 1
    if pages_back is None:
        last_page += 1
    if last_page > num_pages:
        last_page = num_pages
    if last_page < num_pages:
        pages_forward = last_page + half_page_num
        if pages_forward > num_pages:
            pages_forward = num_pages
    else:
        pages_forward = None
        if first_page > 1:
            first_page -= 1
        if pages_back > 1:
            pages_back -= 1
        else:
            pages_back = None
    pages_shown = []
    for i in range(first_page, last_page + 1):
        pages_shown.append(i)
    # Append proper character to url
    if url:
        # Remove existing page GET parameters
        url = unicode(url)
        url = re.sub(r'\?page\=[^\&]+', u'?', url)
        url = re.sub(r'\&page\=[^\&]+', u'', url)
        # Append proper separator
        if u'?' in url:
            url += u'&'
        else:
            url += u'?'
    # Append extra string to url
    if extra:
        if not url:
            url = u'?'
        url += unicode(extra) + u'&'
    if url:
        url = url.replace(u'?&', u'?')
    # Build context object
    return {
        'bootstrap_pagination_url': url,
        'num_pages': num_pages,
        'current_page': current_page,
        'first_page': first_page,
        'last_page': last_page,
        'pages_shown': pages_shown,
        'pages_back': pages_back,
        'pages_forward': pages_forward,
    }
