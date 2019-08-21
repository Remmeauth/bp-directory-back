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
    username = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput)


class ChangeUserPasswordForm(forms.Form):
    """
    Change user password form implementation.
    """

    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)


class ChangeUserEmailForm(forms.Form):
    """
    Change user e-mail form implementation.
    """

    new_email = forms.EmailField()


class UpdateProfileForm(forms.Form):
    """
    Update user profile form implementation.
    """

    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=100)
    email = forms.EmailField(required=False)
    location = forms.CharField(required=False, max_length=100)
    avatar_url = forms.URLField(required=False, max_length=200)
    additional_information = forms.CharField(required=False, widget=forms.Textarea)

    website_url = forms.URLField(required=False, max_length=200)
    linkedin_url = forms.URLField(required=False, max_length=200)
    twitter_url = forms.URLField(required=False, max_length=200)
    medium_url = forms.URLField(required=False, max_length=200)
    github_url = forms.URLField(required=False, max_length=200)
    facebook_url = forms.URLField(required=False, max_length=200)
    telegram_url = forms.URLField(required=False, max_length=200)
    steemit_url = forms.URLField(required=False, max_length=200)


class UploadUserAvatarForm(forms.Form):
    """
    Upload user avatar form implementation.
    """

    title = forms.CharField(max_length=150)
    file = forms.FileField()
