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


class BootstrapInput(forms.TextInput):

    bootstrap = {
                 'append': None,
                 'prepend': None
                 }
    attrs = {}

    def __init__(self, attrs=None, bootstrap_attrs=None):
        if bootstrap_attrs is not None:
            self.bootstrap.update(bootstrap_attrs)
        if attrs is not None:
            self.attrs = self.build_attrs(attrs)
        super(BootstrapInput, self).__init__(self.attrs)

        print 'BootstrapInput.__init__', self.bootstrap, self.attrs

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = dict(self.attrs, **kwargs)
        if extra_attrs:
            if 'class' in extra_attrs and 'class' in attrs:
                attrs['class'] = add_to_css_class(attrs['class'],
                                                  extra_attrs.pop('class'))
            attrs.update(extra_attrs)
        return attrs

    def render(self, name, value, attrs=None):
        css_class = []
        prepend = ''
        append = ''
        final_attrs = self.build_attrs(attrs)
        if self.bootstrap['prepend']:
            css_class.append('input-prepend')
            prepend = '<span class="add-on">%s</span>' % (
                self.bootstrap['prepend']
            )
        if self.bootstrap['append']:
            css_class.append('input-append')
            append = '<span class="add-on">%s</span>' % (
                self.bootstrap['append']
            )

        return mark_safe('<div class="%s">%s%s%s</div>' % (
            u' '.join(css_class),
            prepend,
            super(BootstrapInput, self).render(name, value, final_attrs),
            append,
        ))


class BootstrapDateInput(BootstrapInput, forms.DateInput):

    bootstrap = {
        'append': None,
        'prepend': mark_safe('<i class="icon-calendar"></i>'),
    }
    attrs = {
        'class': 'datepicker'
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


class BootstrapTimeInput(BootstrapInput, forms.TimeInput):

    bootstrap = {
        'append': None,
        'prepend': mark_safe('<i class="icon-time"></i>')
    }
    attrs = {
        'class': 'timepicker'
    }

    class Media:
        js = (
            settings.STATIC_URL + 'timepicker/js/bootstrap-timepicker.js',
            settings.STATIC_URL + 'bootstrap_toolkit/js/init_timepicker.js',
        )
        css = {
            'screen': (
                settings.STATIC_URL + 'timepicker/css/timepicker.css',
            )
        }


class BootstrapDateTimeInput(forms.SplitDateTimeWidget):

    def __init__(self, attrs=None):
        widgets = [
                   BootstrapDateInput(attrs={'class': 'input-small',
                                             'style': 'margin-right: 15px;'}),
                   BootstrapTimeInput(attrs={'class': 'input-mini'})]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)
