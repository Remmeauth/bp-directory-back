"""
Provide database models for user.
"""
from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User database model.
    """

    name = models.CharField(_('name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=100, blank=False)
    email = models.EmailField(_('email'), unique=True, blank=False)

    created = models.DateTimeField(_('created'), auto_now_add=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        """
        Meta.
        """

        ordering = ('created',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the first name plus the last name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.name

    @classmethod
    def create_with_email(cls, email, password):
        """
        Create a user with specified e-mail address and password.
        """
        cls.objects.create(email=email, password=password)

    @classmethod
    def does_exist(cls, email):
        """
        Check if user exists by e-mail address.
        """
        if cls.objects.filter(email=email).exists():
            return True

        return False
