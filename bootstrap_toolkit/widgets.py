from django import forms
from django.forms.util import to_current_timezone
from django.conf import settings
from django.utils import translation
from django.utils.safestring import mark_safe

default_date_format = getattr(settings, 'DATE_INPUT_FORMATS', None)
if default_date_format:
    default_date_format = str(default_date_format[0])

default_time_format = getattr(settings, 'TIME_INPUT_FORMATS', None)
if default_time_format:
    default_time_format = str(default_time_format[0])

def javascript_date_format(python_date_format):
    format = python_date_format.replace(r'%Y', 'yyyy')
    format = format.replace(r'%m', 'mm')
    format = format.replace(r'%d', 'dd')
    if '%' in format:
        format = ''
    if not format:
        format = 'yyyy-mm-dd'
    return format


def javascript_time_format(python_time_format):
    format = python_time_format.replace(r'%H', 'HH')
    format = format.replace(r'%M', 'MM')
    format = format.replace(r'%S', 'SS')
    if '%' in format:
        format = ''
    if not format:
        format = 'HH:MM:SS'
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


class BootstrapUneditableInput(forms.TextInput):

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['type'] = 'hidden'
        klass = add_to_css_class(self.attrs.pop('class', ''), 'uneditable-input')
        klass = add_to_css_class(klass, attrs.pop('class', ''))
        base = super(BootstrapUneditableInput, self).render(name, value, attrs)
        return mark_safe(base + u'<span class="%s">%s</span>' % (klass, value))


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

    class Media:
        js = (
            settings.STATIC_URL + 'datepicker/js/bootstrap-datepicker.js',
        )
        lang = translation.get_language().split('-')[0].lower()
        if lang != 'en':
            js = js + (
                settings.STATIC_URL + 'datepicker/js/locales/bootstrap-datepicker.%s.js' % lang,
            )
        js = js + (
            settings.STATIC_URL + 'bootstrap_toolkit/js/init_datepicker.js',
        )
        css = {
            'screen': (
                settings.STATIC_URL + 'datepicker/css/datepicker.css',
            )
        }

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        format = self.format
        if not format:
            format = default_date_format
        attrs['data-date-format'] = javascript_date_format(format)
        attrs['data-date-language'] = translation.get_language().split('-')[0].lower()
        attrs['data-bootstrap-widget'] = 'datepicker'
        return super(BootstrapDateInput, self).render(name, value, attrs)

class BootstrapTimeInput(forms.TimeInput):

    bootstrap = {
        'append': mark_safe('<i class="icon-time"></i>'),
        'prepend': None,
    }

    class Media:
        js = (
            settings.STATIC_URL + 'timepicker/js/bootstrap-timepicker.js',
        )
        lang = translation.get_language().split('-')[0].lower()
        if lang != 'en':
            js = js + (
                settings.STATIC_URL + 'timepicker/js/locales/bootstrap-timepicker.%s.js' % lang,
            )
        js = js + (
            settings.STATIC_URL + 'bootstrap_toolkit/js/init_timepicker.js',
        )
        css = {
            'screen': (
                settings.STATIC_URL + 'timepicker/css/timepicker.css',
            )
        }

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        format = self.format
        if not format:
            format = default_time_format
        attrs['data-time-format'] = javascript_time_format(format)
        attrs['data-time-language'] = translation.get_language().split('-')[0].lower()
        attrs['data-bootstrap-widget'] = 'timepicker'
        return super(BootstrapTimeInput, self).render(name, value, attrs)


class BootstrapDateTimeInput(forms.MultiWidget):

    def __init__(self, attrs=None):
        widgets = (BootstrapDateInput(attrs=attrs),
                   BootstrapTimeInput(attrs=attrs))
        super(BootstrapDateTimeInput, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]
