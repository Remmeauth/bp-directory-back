"""
Provide implementation of single block producer like endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.decorators import authentication_classes
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from block_producer.domain.errors import BlockProducerWithSpecifiedIdentifierDoesNotExistError
from block_producer.domain.objects import LikeBlockProducer
from block_producer.models import (
    BlockProducer,
    BlockProducerLike,
)
from user.domain.errors import UserWithSpecifiedEmailAddressDoesNotExistError
from user.models import User


class BlockProducerLikeSingle(APIView):
    """
    Single block producer like endpoint implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.block_producer = BlockProducer()
        self.block_producer_like = BlockProducerLike()

    @authentication_classes((JSONWebTokenAuthentication, ))
    def post(self, request, block_producer_id):
        """
        To like the block producer.
        """
        email = request.user.email

        try:
            LikeBlockProducer(
                user=self.user, block_producer=self.block_producer, block_producer_like=self.block_producer_like,
            ).do(
                user_email=email, block_producer_id=block_producer_id,
            )
        except (
                BlockProducerWithSpecifiedIdentifierDoesNotExistError,
                UserWithSpecifiedEmailAddressDoesNotExistError,
        ) as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'Block producer liking has been handled.'}, status=HTTPStatus.OK)
