from django import forms

from docs.models import Doc


class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "autofocus": "on",
                "type": "search",
                "placeholder": "Type to search...",
                "autocompelete": "off",
            }
        ),
    )


class UplaodDocumentForm(forms.ModelForm):
    class Meta:
        model = Doc
        fields = ["file"]
