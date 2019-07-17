"""
Provide configuration for admin panel user tables.
"""
from django.contrib import admin

from user.models import User

admin.site.register(User)
