"""Forms used by the shop app."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


def _styled_text_input(placeholder: str) -> forms.TextInput:
    return forms.TextInput(
        attrs={
            "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none",
            "placeholder": placeholder,
        }
    )


def _styled_password_input(placeholder: str) -> forms.PasswordInput:
    return forms.PasswordInput(
        attrs={
            "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none",
            "placeholder": placeholder,
        }
    )


def _styled_email_input(placeholder: str) -> forms.EmailInput:
    return forms.EmailInput(
        attrs={
            "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none",
            "placeholder": placeholder,
        }
    )


class StyledAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=_styled_text_input("Enter your username"))
    password = forms.CharField(widget=_styled_password_input("Enter your password"))


class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=_styled_email_input("Enter your email address"))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": _styled_text_input("Choose a username"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = _styled_text_input("Choose a username")
        self.fields["password1"].widget = _styled_password_input("Create a password")
        self.fields["password2"].widget = _styled_password_input("Confirm your password")

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user