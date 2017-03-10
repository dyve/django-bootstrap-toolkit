from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput

class TestForm(forms.Form):
    date = forms.DateField(
        widget=BootstrapDateInput(),
    )
    title = forms.CharField(
        max_length=100,
        help_text=u'This is the standard text input',
    )
    body = forms.CharField(
        max_length=100,
        help_text=u'This is a text area',
        widget=forms.Textarea(
            attrs={
                'title': 'I am "nice"',
            }
        ),
    )
    disabled = forms.CharField(
        max_length=100,
        required=False,
        help_text=u'I am disabled',
        widget=forms.TextInput(attrs={
            'disabled': 'disabled',
            'placeholder': 'I am disabled',
        })
    )
    content = forms.ChoiceField(
        choices=(
            ("text", "Plain text"),
            ("html", "HTML"),
        ),
        help_text=u'Pick your choice',
    )
    email = forms.EmailField()
    like = forms.BooleanField(required=False)
    fruits = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=(
            ("apple", "Apple"),
            ("pear", "Pear"),
        ),
        help_text=u'As you can see, multiple checkboxes work too',
    )
    number = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={
            'inline': True,
        }),
        choices=(
            ("3", "Three"),
            ("33", "Thirty three"),
            ("333", "Three hundred thirty three"),
        ),
        help_text=u'And can be inline',
    )
    color = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'data-demo-attr': 'bazinga'}),
        choices=(
            ("#f00", "red"),
            ("#0f0", "green"),
            ("#00f", "blue"),
        ),
        help_text=u'And we have <i>radiosets</i>',
    )
    prepended = forms.CharField(
        max_length=100,
        help_text=u'I am prepended by a P',
        widget=BootstrapTextInput(prepend='P'),
    )

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data


class TestModelForm(forms.ModelForm):
    class Meta:
        model = User


class TestInlineForm(forms.Form):
    query = forms.CharField(
        required=True, 
        label='', 
        widget=forms.TextInput(attrs={
            'placeholder': "Query"
        }))
    vegetable = forms.ChoiceField(
        label='', 
        choices=(
            ("broccoli", "Broccoli"),
            ("carrots", "Carrots"),
            ("turnips", "Turnips"),
        ))
    active = forms.ChoiceField(
        label='', 
        choices=(
            ('all', 'all'),
            ('active', 'active'),
            ('inactive', 'inactive')), 
        initial='all')
    mine = forms.BooleanField(label='Mine only', initial=False, required=True)


class WidgetsForm(forms.Form):
    date = forms.DateField(widget=BootstrapDateInput)


class FormSetInlineForm(forms.Form):
    foo = forms.CharField(
        help_text=u'This is the standard text input',
        widget=forms.TextInput(attrs={
            'placeholder': "Foo"
        }))
    bar = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': "Bar"
        }))
    vegetable = forms.ChoiceField(
        choices=(
            ("broccoli", "Broccoli"),
            ("carrots", "Carrots"),
            ("turnips", "Turnips"),
        ))


