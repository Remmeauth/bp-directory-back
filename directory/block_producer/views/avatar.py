"""
Provide implementation of single block producer avatar endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.decorators import authentication_classes
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from block_producer.domain.errors import BlockProducerWithSpecifiedIdentifierDoesNotExistError
from block_producer.domain.objects import UpdateBlockProducer
from block_producer.forms import UploadBlockProducerAvatarForm
from block_producer.models import BlockProducer
from services.avatar import (
    Avatar,
    AvatarTypes,
)
from user.domain.errors import UserWithSpecifiedEmailAddressDoesNotExistError
from user.models import User


class BlockProducerAvatarSingle(APIView):
    """
    Single block producer avatar implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.block_producer = BlockProducer()

    @authentication_classes((JSONWebTokenAuthentication, ))
    def post(self, request, block_producer_id):
        """
        Upload block producer avatar.
        """
        user_email = request.user.email

        form = UploadBlockProducerAvatarForm(request.POST, request.FILES)

        if form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        file_to_upload = request.FILES.get('file')
        file_to_upload_name = str(block_producer_id)

        avatar = Avatar(name=file_to_upload_name, type_=AvatarTypes.block_producer)
        avatar.upload(file_object=file_to_upload)

        try:
            UpdateBlockProducer(
                user=self.user, block_producer=self.block_producer,
            ).do(
                user_email=user_email,
                block_producer_id=block_producer_id,
                info={'logo_url': avatar.get_url()},
            )

        except (
            BlockProducerWithSpecifiedIdentifierDoesNotExistError,
            UserWithSpecifiedEmailAddressDoesNotExistError,
        ) as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.NOT_FOUND)

        return JsonResponse({'result': 'Block producer avatar has been uploaded.'}, status=HTTPStatus.OK)
