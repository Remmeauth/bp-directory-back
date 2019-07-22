"""
Provide database models for block producer.
"""
from __future__ import unicode_literals

from django.db import models

from user.models import User


class BlockProducer(models.Model):
    """
    Block producer database model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, null=False, blank=False)
    website_url = models.URLField(max_length=200, null=False, blank=False)
    location = models.CharField(max_length=100, blank=True)
    short_description = models.CharField(max_length=100, null=False, blank=False)
    full_description = models.TextField(blank=True)
    logo_url = models.URLField(max_length=200, blank=True)

    linkedin_url = models.URLField(max_length=200, blank=True)
    twitter_url = models.URLField(max_length=200, blank=True)
    medium_url = models.URLField(max_length=200, blank=True)
    github_url = models.URLField(max_length=200, blank=True)
    facebook_url = models.URLField(max_length=200, blank=True)
    telegram_url = models.URLField(max_length=200, blank=True)
    reddit_url = models.URLField(max_length=200, blank=True)
    slack_url = models.URLField(max_length=200, blank=True)
    wikipedia_url = models.URLField(max_length=200, blank=True)
    steemit_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        """
        Get string representation of an object.
        """
        return f'{self.name} — {self.user.email}'
