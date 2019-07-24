"""
Provide implementation of operation with block producer forms.
"""
from django import forms


class CreateBlockProducerForm(forms.Form):
    """
    Create block producer form implementation.
    """

    name = forms.CharField(required=True)
    website_url = forms.URLField(required=True)
    location = forms.CharField(required=False)
    short_description = forms.CharField(required=True)
    full_description = forms.CharField(widget=forms.Textarea, required=False)
    logo_url = forms.URLField(required=False)

    linkedin_url = forms.URLField(required=False)
    twitter_url = forms.URLField(required=False)
    medium_url = forms.URLField(required=False)
    github_url = forms.URLField(required=False)
    facebook_url = forms.URLField(required=False)
    telegram_url = forms.URLField(required=False)
    reddit_url = forms.URLField(required=False)
    slack_url = forms.URLField(required=False)
    wikipedia_url = forms.URLField(required=False)
    steemit_url = forms.URLField(required=False)
