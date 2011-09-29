from django import forms

class TestForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        help_text=u'And we have radiosets',
    )
    content = forms.CharField()
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
    color = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            ("#f00", "red"),
            ("#0f0", "green"),
            ("#00f", "blue"),
        ),
        help_text=u'And we have radiosets',
    )