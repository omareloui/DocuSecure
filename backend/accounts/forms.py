from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(min_length=2)
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(required=False, widget=forms.HiddenInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]

    def clean(self):
        clean_data = super().clean()
        password = clean_data.get("password")
        password_confirm = clean_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return clean_data
