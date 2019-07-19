"""
Provide implementation of user endpoints .
"""
from django.urls import path

from user.views.registration import UserRegistrationSingle

user_endpoints = [
    path('registration/', UserRegistrationSingle.as_view()),
]
