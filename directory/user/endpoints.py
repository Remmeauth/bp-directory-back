"""
Provide implementation of user endpoints.
"""
from django.urls import path

from user.views.email import UserEmailSingle
from user.views.password import (
    UserPasswordRecoverSingle,
    UserPasswordSingle,
    UserRequestPasswordRecoverySingle,
)
from user.views.profile import UserProfileSingle
from user.views.registration import UserRegistrationSingle
from user.views.user import (
    UserFromTokenSingle,
    UserSingle,
)

user_endpoints = [
    path('', UserFromTokenSingle.as_view()),
    path('<str:username>/password/', UserPasswordSingle.as_view()),
    path('password/recovery/', UserRequestPasswordRecoverySingle.as_view()),
    path('password/recovery/<user_identifier>/', UserPasswordRecoverSingle.as_view()),
    path('registration/', UserRegistrationSingle.as_view()),
    path('<str:username>/', UserSingle.as_view()),
    path('<str:username>/profile/', UserProfileSingle.as_view()),
    path('<str:username>/email/', UserEmailSingle.as_view()),
]
