"""
Provide implementation of root endpoints.
"""
from django.contrib import admin
from django.urls import (
    include,
    path,
)
from rest_framework_jwt.views import (
    ObtainJSONWebToken,
    refresh_jwt_token,
    verify_jwt_token,
)

from block_producer.endpoints import block_producer_endpoints
from generic.jwt import CustomJWTSerializer
from user.endpoints import user_endpoints

authentication_endpoints = [
    path('token/obtaining/', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)),
    path('token/refreshing/', refresh_jwt_token),
    path('token/verification/', verify_jwt_token),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include(authentication_endpoints)),
    path('user/', include(user_endpoints)),
    path('block-producers/', include(block_producer_endpoints)),
]
