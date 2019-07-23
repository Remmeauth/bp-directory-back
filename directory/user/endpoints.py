"""
Provide implementation of user endpoints.
"""
from django.urls import path

from user.views.password import (
    UserPasswordRecoverySingle,
    UserPasswordSingle,
    UserRequestPasswordRecoverySingle,
)
from user.views.registration import UserRegistrationSingle

user_endpoints = [
    path('password/', UserPasswordSingle.as_view()),
    path('password/recovery/', UserRequestPasswordRecoverySingle.as_view()),
    path('password/recovery/<user_identifier>', UserPasswordRecoverySingle.as_view()),
    path('registration/', UserRegistrationSingle.as_view()),
]
