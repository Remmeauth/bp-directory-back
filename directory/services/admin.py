"""
Provide configuration for admin panel services tables.
"""
from django.contrib import admin

from services.models import PasswordRecoveryState

admin.site.register(PasswordRecoveryState)
