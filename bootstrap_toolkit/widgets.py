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

def convert_date_format(format):
    format = format.replace('%m', 'mm')
    format = format.replace('%d', 'dd')
    format = format.replace('%Y', 'yyyy')
    format = format.replace('%y', 'yy')
    return format

class BootstrapDateInput(forms.DateInput):

    bootstrap = {
        'append': mark_safe('<i class="icon-calendar"></i>'),
        'prepend': None,
    }

    def __init__(self, attrs=None, format=None):
        super(BootstrapDateInput, self).__init__(attrs, format)
        self.attrs['data-date-format'] = convert_date_format(str(self.format))

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
