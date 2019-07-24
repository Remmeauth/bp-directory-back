"""
Provide database models for password recovery state.
"""
from django.db import models


class PasswordRecoveryState(models.Model):
    """
    Password recovery state database model.
    """

    email = models.EmailField(blank=False)
    identifier = models.UUIDField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        Get string representation of an object.
        """
        return f'{self.created_at} — {self.email}'

    @classmethod
    def create(cls, email, identifier):
        """
        Create password recovery state with e-mail and identifier.
        """
        cls.objects.create(email=email, identifier=identifier)

    @classmethod
    def does_exist(cls, user_identifier):
        """
        Check if user exists by identifier.
        """
        if cls.objects.filter(identifier=user_identifier).exists():
            return True

        return False

    @classmethod
    def get_email(cls, user_identifier):
        """
        Get email by existing user identifier.
        """
        return cls.objects.get(identifier=user_identifier).email

    @classmethod
    def is_active_(cls, user_identifier):
        """
        Check if user exists by identifier.
        """
        if cls.objects.get(identifier=user_identifier).is_active:
            return True

        return False

    @classmethod
    def deactivate(cls, user_identifier):
        """
        Deactivate password recovery state.
        """
        password_recovery_state = cls.objects.get(identifier=user_identifier)
        password_recovery_state.is_active = False
        password_recovery_state.save()
