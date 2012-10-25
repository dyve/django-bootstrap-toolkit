from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

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


class BootstrapTextInput(forms.TextInput):
    bootstrap = {}

    def __init__(self, *args, **kwargs):
        self.bootstrap['append'] = kwargs.pop('append', None)
        self.bootstrap['prepend'] = kwargs.pop('prepend', None)
        super(BootstrapTextInput, self).__init__(*args, **kwargs)


class BootstrapDateInput(forms.DateInput):

    bootstrap = {
        'append': mark_safe('<i class="icon-calendar"></i>'),
        'prepend': None,
    }

    def __init__(self, *args, **kwargs):
        if 'popup_date_format' in kwargs:
            date_format = kwargs.pop('popup_date_format')
            if not 'attrs' in kwargs or kwargs['attrs'] is None:
                kwargs['attrs'] = {}
            if date_format:
                kwargs['attrs']['data-date-format'] = date_format

        super(BootstrapDateInput, self).__init__(*args, **kwargs)

    class Media:
        js = (
            settings.STATIC_URL + 'datepicker/js/bootstrap-datepicker.js',
            settings.STATIC_URL + 'bootstrap_toolkit/js/init_datepicker.js',
        )
        css = {
            'screen': (
                settings.STATIC_URL + 'datepicker/css/datepicker.css',
            )
        }

    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        if 'class' in attrs:
            attrs['class'] = add_to_css_class(attrs['class'], 'datepicker-widget')
        else:
            attrs['class'] = 'datepicker-widget'
        return super(BootstrapDateInput, self).render(name, value, attrs)
