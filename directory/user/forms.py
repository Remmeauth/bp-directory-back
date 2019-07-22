"""
Provide implementation of operation with user forms.
"""
from django import forms


class RestoreUserPasswordForm(forms.Form):
    """
    Restore user password form implementation.
    """

    email = forms.EmailField()


class UserRegistrationForm(forms.Form):
    """
    Register user form implementation.
    """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ChangeUserPasswordForm(forms.Form):
    """
    Change user password form implementation.
    """

    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
