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


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class BulkUpload(forms.Form):
    files = MultipleFileField()
