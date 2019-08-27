"""
Provide implementation of operation with block producer forms.
"""
from django import forms


class CreateBlockProducerForm(forms.Form):
    """
    Create block producer form implementation.
    """

    name = forms.CharField(required=True, max_length=50)
    website_url = forms.URLField(required=True, max_length=200)
    location = forms.CharField(required=False, max_length=100)
    short_description = forms.CharField(required=True, max_length=100)
    full_description = forms.CharField(widget=forms.Textarea, required=False)
    logo_url = forms.URLField(required=False, max_length=200)

    linkedin_url = forms.URLField(required=False, max_length=200)
    twitter_url = forms.URLField(required=False, max_length=200)
    medium_url = forms.URLField(required=False, max_length=200)
    github_url = forms.URLField(required=False, max_length=200)
    facebook_url = forms.URLField(required=False, max_length=200)
    telegram_url = forms.URLField(required=False, max_length=200)
    reddit_url = forms.URLField(required=False, max_length=200)
    slack_url = forms.URLField(required=False, max_length=200)
    wikipedia_url = forms.URLField(required=False, max_length=200)
    steemit_url = forms.URLField(required=False, max_length=200)


class UpdateBlockProducerForm(forms.Form):
    """
    Update block producer form implementation.
    """

    name = forms.CharField(required=False, max_length=50)
    website_url = forms.URLField(required=False, max_length=200)
    location = forms.CharField(required=False, max_length=100)
    short_description = forms.CharField(required=False, max_length=100)
    full_description = forms.CharField(widget=forms.Textarea, required=False)
    logo_url = forms.URLField(required=False, max_length=200)

    linkedin_url = forms.URLField(required=False, max_length=200)
    twitter_url = forms.URLField(required=False, max_length=200)
    medium_url = forms.URLField(required=False, max_length=200)
    github_url = forms.URLField(required=False, max_length=200)
    facebook_url = forms.URLField(required=False, max_length=200)
    telegram_url = forms.URLField(required=False, max_length=200)
    reddit_url = forms.URLField(required=False, max_length=200)
    slack_url = forms.URLField(required=False, max_length=200)
    wikipedia_url = forms.URLField(required=False, max_length=200)
    steemit_url = forms.URLField(required=False, max_length=200)


class UploadBlockProducerAvatarForm(forms.Form):
    """
    Upload block producer avatar form implementation.
    """

    title = forms.CharField(max_length=150)
    file = forms.FileField()
