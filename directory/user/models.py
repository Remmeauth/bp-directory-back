"""
Provide database models for user.
"""
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from services.models import EmailConfirmState
from user.dto.profile import UserProfileDto
from user.dto.user import UserDto
from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User database model.
    """

    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(unique=True, max_length=25, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    is_email_confirmed = models.BooleanField(default=False)

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
        user = cls.objects.create_user(email=email, username=username, password=password)
        Profile.objects.create(user=user)

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
    def set_new_email(cls, username, email):
        """
        Set new user e-mail by specified username.
        """
        user = cls.objects.get(username=username)
        user.email = email
        user.save()

    @classmethod
    def is_email_confirmed_(cls, user_identifier):
        """
        Check if user email confirmed by identifier.
        """
        email = EmailConfirmState.get_email(user_identifier=user_identifier)
        if cls.objects.get(email=email).is_email_confirmed:
            return True

        return False

    @classmethod
    def set_email_as_confirmed(cls, user_identifier):
        """
        Set email as confirmed by identifier.
        """
        email = EmailConfirmState.get_email(user_identifier=user_identifier)
        user_state = cls.objects.get(email=email)
        user_state.is_email_confirmed = True
        user_state.save()


class Profile(models.Model):
    """
    Profile database model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar_url = models.URLField(max_length=200, blank=True, default=settings.DEFAULT_USER_LOGOTYPE_URL)
    additional_information = models.TextField(blank=True)

    website_url = models.URLField(max_length=200, blank=True)
    linkedin_url = models.URLField(max_length=200, blank=True)
    twitter_url = models.URLField(max_length=200, blank=True)
    medium_url = models.URLField(max_length=200, blank=True)
    github_url = models.URLField(max_length=200, blank=True)
    facebook_url = models.URLField(max_length=200, blank=True)
    telegram_url = models.URLField(max_length=200, blank=True)
    steemit_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        """
        Get string representation of an object.
        """
        return self.user.email

    @classmethod
    def update(cls, username, info):
        """
        Update user profile with specified information.
        """
        user = User.objects.get(username=username)
        cls.objects.filter(user=user).update(**info)

    @classmethod
    def get(cls, username):
        """
        Get user profile information by username.
        """
        user = User.objects.get(username=username)
        user_profile_as_dict = cls.objects.filter(user=user).values().first()

        user_as_dict = User.objects.filter(username=username).values().first()

        del user_as_dict['password']
        del user_as_dict['created']

        user_profile_as_dict['user'] = user_as_dict

        return UserProfileDto(**user_profile_as_dict)
