from django import forms

from docs.models import Doc


class DocumentForm(forms.Form):
    title = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea)

    def save(self):
        doc = Doc(
            title=self.cleaned_data.get("title"),
            content=self.cleaned_data.get("content"),
        )
        doc.save()
