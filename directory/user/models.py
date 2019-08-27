"""
Provide database models for user.
"""
from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from user.dto.user import UserDto
from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User database model.
    """

    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(unique=True, max_length=25, blank=False)

    created = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

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
        return self.username

    @classmethod
    def create_with_email(cls, email, username, password):
        """
        Create a user with specified e-mail address and password.
        """
        cls.objects.create_user(email=email, username=username, password=password)

    @classmethod
    def does_exist_by_email(cls, email):
        """
        Check if user exists by e-mail address.
        """
        if cls.objects.filter(email=email).exists():
            return True

        return False

    @classmethod
    def does_exist_by_username(cls, username):
        """
        Check if user exists by username.
        """
        if cls.objects.filter(username=username).exists():
            return True

        return False

    @classmethod
    def verify_password(cls, email, password):
        """
        Check if the user's password is equal to the encrypted user password.
        """
        encrypted_user_password = cls.objects.get(email=email).password
        return check_password(password=password, encoded=encrypted_user_password)

    @classmethod
    def set_new_password(cls, email, password):
        """
        Set new user password by specified e-mail.
        """
        user = cls.objects.get(email=email)
        user.set_password(password)
        user.save()

    @classmethod
    def get(cls, username):
        """
        Get user.
        """
        user_as_dict = cls.objects.filter(username=username).values().first()
        del user_as_dict['password']
        del user_as_dict['created']
        return UserDto(**user_as_dict)

    @classmethod
    def delete_(cls, username):
        """
        Delete user.
        """
        cls.objects.filter(username=username).delete()

    @classmethod
    def set_new_email(cls, user_email, new_email):
        """
        Set new user e-mail by specified username.
        """
        user = cls.objects.get(email=user_email)
        user.email = new_email
        user.save()
