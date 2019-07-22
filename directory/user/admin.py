"""
Provide configuration for admin panel user tables.
"""
from django.contrib import admin

from user.models import (
    Profile,
    User,
)

admin.site.register(Profile)
admin.site.register(User)
