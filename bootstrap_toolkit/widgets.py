from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.contrib.staticfiles import finders


default_date_format = getattr(settings, 'DATE_INPUT_FORMATS', None)
if default_date_format:
    default_date_format = str(default_date_format[0])


def javascript_date_format(python_date_format):
    format = python_date_format.replace(r'%Y', 'yyyy')
    format = format.replace(r'%m', 'mm')
    format = format.replace(r'%d', 'dd')
    if '%' in format:
        format = ''
    if not format:
        format = 'yyyy-mm-dd'
    return format


def add_to_css_class(classes, new_class):
    new_class = new_class.strip()
    if new_class:
        # Turn string into list of classes
        classes = classes.split(" ")
        # Strip whitespace
        classes = [c.strip() for c in classes]
        # Remove empty elements
        classes = filter(None, classes)
        # Test for existing
        if not new_class in classes:
            classes.append(new_class)
            # Convert to string
        classes = u" ".join(classes)
    return classes


def create_prepend_append(**kwargs):
    bootstrap = {}
    bootstrap['append'] = kwargs.pop('append', None)
    bootstrap['prepend'] = kwargs.pop('prepend', None)
    return bootstrap, kwargs


def get_language():
    lang = translation.get_language()
    if '-' in lang:
        lang = "%s-%s" % (lang.split('-')[0].lower(), lang.split('-')[1].upper())
    return lang


def get_locale_js_url(lang):
    url = 'datepicker/js/locales/bootstrap-datepicker.%s.js' % lang
    if finders.find(url):
        return settings.STATIC_URL + url
    if '-' in lang:
        return get_locale_js_url(lang.split('-')[0].lower())
    return ''


class BootstrapUneditableInput(forms.TextInput):

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['type'] = 'hidden'
        klass = add_to_css_class(self.attrs.pop('class', ''), 'uneditable-input')
        klass = add_to_css_class(klass, attrs.pop('class', ''))
        base = super(BootstrapUneditableInput, self).render(name, value, attrs)
        return mark_safe(base + u'<span class="%s">%s</span>' % (klass, conditional_escape(value)))


class BootstrapTextInput(forms.TextInput):

    def __init__(self, *args, **kwargs):
        self.bootstrap, kwargs = create_prepend_append(**kwargs)
        super(BootstrapTextInput, self).__init__(*args, **kwargs)


class BootstrapPasswordInput(forms.PasswordInput):

    def __init__(self, *args, **kwargs):
        self.bootstrap, kwargs = create_prepend_append(**kwargs)
        super(BootstrapPasswordInput, self).__init__(*args, **kwargs)


class BootstrapDateInput(forms.DateInput):

    bootstrap = {
        'append': mark_safe('<i class="icon-calendar"></i>'),
        'prepend': None,
    }

    @property
    def media(self):
        js = (
            settings.STATIC_URL + 'datepicker/js/bootstrap-datepicker.js',
        )
        lang = get_language()
        if lang != 'en':
            locale_js_url = get_locale_js_url(lang)
            if locale_js_url:
                js = js + (
                    locale_js_url,
                )
        js = js + (
            settings.STATIC_URL + 'bootstrap_toolkit/js/init_datepicker.js',
        )
        css = {
            'screen': (
                settings.STATIC_URL + 'datepicker/css/datepicker.css',
            )
        }
        return forms.Media(css=css, js=js)

    def render(self, name, value, attrs=None):
        date_input_attrs = {}
        if attrs:
            date_input_attrs.update(attrs)
        date_format = self.format
        if not date_format:
            date_format = default_date_format
        date_input_attrs.update({
            'data-date-format': javascript_date_format(date_format),
            'data-date-language': get_language(),
            'data-bootstrap-widget': 'datepicker',
        })
        return super(BootstrapDateInput, self).render(name, value, attrs=date_input_attrs)
