"""
Provide implementation of single user password endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
)
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user.domain.errors import UserWithSpecifiedUsernameDoesNotExistError
from user.domain.objects import DeleteUser
from user.models import User


class UserSingle(APIView):
    """
    Single user endpoint implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()

    @permission_classes((JSONWebTokenAuthentication, ))
    def get(self, request):
        """
        Get user.
        """
        return JsonResponse({'result': {
            'email': request.user.email,
        }}, status=HTTPStatus.OK)

    @authentication_classes((JSONWebTokenAuthentication, ))
    def delete(self, request):
        """
        Delete user.
        """
        user_username = request.user.username

        try:
            DeleteUser(user=self.user).do(username=user_username)
        except UserWithSpecifiedUsernameDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.NOT_FOUND)

        return JsonResponse({'result': 'User has been deleted.'}, status=HTTPStatus.OK)
