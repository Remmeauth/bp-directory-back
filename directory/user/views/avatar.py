"""
Provide implementation of single user avatar endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.decorators import authentication_classes
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from services.avatar import (
    Avatar,
    AvatarTypes,
)
from user.domain.errors import UserHasNoAuthorityToUpdateThisUserProfileError
from user.domain.objects import UpdateUserProfile
from user.forms import UploadUserAvatarForm
from user.models import (
    Profile,
    User,
)


class UserAvatarSingle(APIView):
    """
    Single user avatar implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.profile = Profile()

    @authentication_classes((JSONWebTokenAuthentication, ))
    def post(self, request, username):
        """
        Upload user avatar.
        """
        if username != request.user.username:
            return JsonResponse(
                {'error': UserHasNoAuthorityToUpdateThisUserProfileError().message}, status=HTTPStatus.BAD_REQUEST,
            )

        form = UploadUserAvatarForm(request.POST, request.FILES)

        if form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        file_to_upload = request.FILES.get('file')
        file_to_upload_name = str(request.user.id)

        avatar = Avatar(name=file_to_upload_name, type_=AvatarTypes.user)
        avatar.upload(file_object=file_to_upload)

        UpdateUserProfile(user=self.user, profile=self.profile).do(
            username=username, info={'avatar_url': avatar.get_url()},
        )

        return JsonResponse({'result': 'User avatar has been uploaded.'}, status=HTTPStatus.OK)
