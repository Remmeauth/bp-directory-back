"""
Provide implementation of single user password endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView

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

    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()

    def get(self, request, username):
        """
        Get user.
        """
        try:
            user = GetUser(user=self.user).do(username=username)
        except UserWithSpecifiedUsernameDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        serialized_user = user.to_dict()
        return JsonResponse({'result': serialized_user}, status=HTTPStatus.OK)

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
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'User has been deleted.'}, status=HTTPStatus.OK)
