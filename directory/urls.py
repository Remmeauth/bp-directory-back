"""
Provide HTTP endpoints as root.
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

authentication_endpoints = [
    path('token/obtaining/', obtain_jwt_token),
    path('token/refreshing/', refresh_jwt_token),
    path('token/verification/', verify_jwt_token),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include(authentication_endpoints)),
]
