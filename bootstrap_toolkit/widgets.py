from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from urls import *

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

class BootstrapDateInput(forms.TextInput):

    bootstrap = {
        'append': mark_safe('<i class="icon-th"></i>'),
        'prepend': None,
    }

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
            attrs['class'] = add_to_css_class(attrs['class'], 'datepicker')
        else:
            attrs['class'] = 'datepicker'
        return super(BootstrapDateInput, self).render(name, value, attrs)
