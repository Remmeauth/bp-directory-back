"""
Provide implementation of single user password endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user.domain.errors import (
    UserHasNoAuthorityToDeleteThisAccountError,
    UserWithSpecifiedUsernameDoesNotExistError,
)
from user.domain.objects import (
    DeleteUser,
    GetUser,
)
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

    @permission_classes((AllowAny, ))
    def get(self, request, username):
        """
        Get user.
        """
        try:
            user = GetUser(user=self.user).do(username=username)
        except UserWithSpecifiedUsernameDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.NOT_FOUND)

        serialized_user = user.to_dict()
        return JsonResponse({'result': serialized_user}, status=HTTPStatus.OK)

    @authentication_classes((JSONWebTokenAuthentication, ))
    def delete(self, request, username):
        """
        Delete user.
        """
        if username != request.user.username:
            return JsonResponse(
                {'error': UserHasNoAuthorityToDeleteThisAccountError().message}, status=HTTPStatus.BAD_REQUEST,
            )

        try:
            DeleteUser(user=self.user).do(username=username)
        except UserWithSpecifiedUsernameDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.NOT_FOUND)

        return JsonResponse({'result': 'User has been deleted.'}, status=HTTPStatus.OK)


class UserFromTokenSingle(APIView):
    """
    Single user from token endpoint implementation.
    """

    @permission_classes((JSONWebTokenAuthentication, ))
    def get(self, request):
        """
        Get user.
        """
        return JsonResponse({'result': {
            'email': request.user.email,
            'username': request.user.username,
        }}, status=HTTPStatus.OK)
