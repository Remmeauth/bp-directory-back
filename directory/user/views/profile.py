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
    UserHasNoAuthorityToUpdateThisUserProfileError,
    UserWithSpecifiedEmailAddressDoesNotExistError,
    UserWithSpecifiedUsernameDoesNotExistError,
)
from user.domain.objects import (
    GetUserProfile,
    UpdateUserProfile,
)
from user.forms import UpdateProfileForm
from user.models import (
    Profile,
    User,
)


class UserProfileSingle(APIView):
    """
    Single user profile endpoint implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.profile = Profile()

    @permission_classes((AllowAny,))
    def get(self, request, username):
        """
        Get user profile.
        """
        try:
            user_profile = GetUserProfile(user=self.user, profile=self.profile).do(username=username)

        except UserWithSpecifiedUsernameDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        serialized_user = user_profile.to_dict()

        return JsonResponse({'result': serialized_user}, status=HTTPStatus.OK)

    @authentication_classes((JSONWebTokenAuthentication, ))
    def post(self, request, username):
        """
        Update user profile.
        """
        if username != request.user.username:
            return JsonResponse(
                {'error': UserHasNoAuthorityToUpdateThisUserProfileError().message}, status=HTTPStatus.BAD_REQUEST,
            )

        form = UpdateProfileForm(request.data)

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        non_empty_request_data = {key: form.cleaned_data[key] for key in request.data}

        try:
            UpdateUserProfile(user=self.user, profile=self.profile).do(username=username, info=non_empty_request_data)

        except UserWithSpecifiedEmailAddressDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'User profile has been updated.'}, status=HTTPStatus.OK)
