"""
Provide implementation of root endpoints.
"""
from django.contrib import admin
from django.urls import (
    include,
    path,
)
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from user.endpoints import user_endpoints

authentication_endpoints = [
    path('token/obtaining/', obtain_jwt_token),
    path('token/refreshing/', refresh_jwt_token),
    path('token/verification/', verify_jwt_token),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include(authentication_endpoints)),
    path('user/', include(user_endpoints)),
]
