from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput

class TestForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        help_text=u'This is the standard text input',
    )
    disabled = forms.CharField(
        max_length=100,
        help_text=u'I am read only',
        widget=forms.TextInput(attrs={
            'disabled': 'disabled'
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
    veggies = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={
            'inline': True,
        }),
        choices=(
            ("broccoli", "Broccoli"),
            ("carrots", "Carrots"),
            ("turnips", "Turnips"),
        ),
        help_text=u'And can be inline',
    )
    color = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            ("#f00", "red"),
            ("#0f0", "green"),
            ("#00f", "blue"),
        ),
        help_text=u'And we have radiosets',
    )

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data

class TestModelForm(forms.ModelForm):
    class Meta:
        model = User

class TestInlineForm(forms.Form):
    query = forms.CharField(required=False, label="")
    active = forms.ChoiceField(widget=forms.RadioSelect, label="", choices=(
        ('all', 'all'),
        ('active', 'active'),
        ('inactive', 'inactive')
        ), initial='all')
    mine = forms.BooleanField(required=False, label='Mine only', initial=False)

class WidgetsForm(forms.Form):
    date = forms.DateField(widget=BootstrapDateInput)