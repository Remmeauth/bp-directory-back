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

from block_producer.views.avatar import BlockProducerAvatarSingle
from block_producer.views.block_producer import (
    BlockProducerCollection,
    BlockProducerSearchCollection,
    BlockProducerSingle,
)
from generic.jwt import CustomJWTSerializer
from user.views.email import UserEmailSingle
from user.views.password import (
    UserPasswordRecoverSingle,
    UserPasswordSingle,
    UserRequestPasswordRecoverySingle,
)
from user.views.registration import UserRegistrationSingle
from user.views.user import (
    UserSingle,
)

authentication_endpoints = [
    path('token/obtaining/', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)),
    path('token/refreshing/', refresh_jwt_token),
    path('token/verification/', verify_jwt_token),
]

user_endpoints = [
    path('', UserSingle.as_view()),
    path('email/', UserEmailSingle.as_view()),
    path('password/', UserPasswordSingle.as_view()),
    path('password/recovery/', UserRequestPasswordRecoverySingle.as_view()),
    path('password/recovery/<user_identifier>/', UserPasswordRecoverSingle.as_view()),
    path('registration/', UserRegistrationSingle.as_view()),

]

block_producer_endpoints = [
    path('', BlockProducerCollection.as_view()),
    path('search/', BlockProducerSearchCollection.as_view()),
    path('<int:block_producer_id>/', BlockProducerSingle.as_view()),
    path('<int:block_producer_id>/avatars/', BlockProducerAvatarSingle.as_view()),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include(authentication_endpoints)),
    path('users/', include(user_endpoints)),
    path('block-producers/', include(block_producer_endpoints)),
]
