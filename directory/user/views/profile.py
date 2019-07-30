"""
Provide implementation of single user password endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user.domain.errors import (
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

    authentication_classes = (JSONWebTokenAuthentication,)

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.profile = Profile()

    def post(self, request):
        """
        Update user profile.
        """
        user_email = request.user.email

        form = UpdateProfileForm(request.data)

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        non_empty_request_data = {key: form.cleaned_data[key] for key in request.data}

        try:
            UpdateUserProfile(user=self.user, profile=self.profile).do(email=user_email, info=non_empty_request_data)
        except UserWithSpecifiedEmailAddressDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'User profile has been updated.'}, status=HTTPStatus.OK)


class GetUserProfileSingle(APIView):
    """
    Single user profile endpoint implementation.
    """

    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.profile = Profile()

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
