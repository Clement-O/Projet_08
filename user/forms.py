from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

# Third party import
from allauth.account.forms import SignupForm

# Local import
from .models import CustomUser

""" Module to create Custom User forms """


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(ModelForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email',)


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = _("Password confirmation")
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': _("password").capitalize()})

    first_name = forms.CharField(
        label=_("first name").capitalize(),
        max_length=30,
        widget=forms.TextInput(
            attrs={'placeholder': _("first name").capitalize()})
    )

    def save(self, request):
        # Ensure you call the parent classes save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original search.
        return user
