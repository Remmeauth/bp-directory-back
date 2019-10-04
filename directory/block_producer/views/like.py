"""
Provide implementation of collection block producer like endpoint.
"""
import json
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
)
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from block_producer.domain.errors import BlockProducerWithSpecifiedIdentifierDoesNotExistError
from block_producer.domain.objects import (
    GetBlockProducerLikes,
    GetBlockProducerLikesNumber,
    LikeBlockProducer,
)
from block_producer.dto.like import (
    BlockProducerLikeDto,
    BlockProducerLikeNumberDto,
)
from block_producer.models import (
    BlockProducer,
    BlockProducerLike,
)
from user.domain.errors import UserWithSpecifiedEmailAddressDoesNotExistError
from user.models import User


class BlockProducerLikeCollection(APIView):
    """
    Collection block producer likes endpoint implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.block_producer = BlockProducer()
        self.block_producer_like = BlockProducerLike()

    @permission_classes((permissions.AllowAny, ))
    def get(self, request, block_producer_id):
        """
        Get block producer's likes.
        """
        block_producer_likes = GetBlockProducerLikes(
            block_producer=self.block_producer, block_producer_like=self.block_producer_like,
        ).do(block_producer_id=block_producer_id)

        serialized_block_producer_likes = json.loads(
            BlockProducerLikeDto.schema().dumps(block_producer_likes, many=True),
        )

        return JsonResponse({'result': serialized_block_producer_likes}, status=HTTPStatus.OK)

    @authentication_classes((JSONWebTokenAuthentication, ))
    def put(self, request, block_producer_id):
        """
        To like the block producer.
        """
        email = request.user.email

        try:
            LikeBlockProducer(
                user=self.user, block_producer=self.block_producer, block_producer_like=self.block_producer_like,
            ).do(user_email=email, block_producer_id=block_producer_id)
        except (
            BlockProducerWithSpecifiedIdentifierDoesNotExistError,
            UserWithSpecifiedEmailAddressDoesNotExistError,
        ) as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.NOT_FOUND)

        return JsonResponse({'result': 'Block producer liking has been handled.'}, status=HTTPStatus.OK)


class BlockProducerLikeNumberCollection(APIView):
    """
    Collection block producer's likes number endpoint implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.block_producer = BlockProducer()
        self.block_producer_like = BlockProducerLike()

    @permission_classes((permissions.AllowAny, ))
    def get(self, request):
        """
        Get block producers' likes number.
        """
        block_producer_likes_number = GetBlockProducerLikesNumber(
            block_producer=self.block_producer,
            block_producer_like=self.block_producer_like,
        ).do()

        serialized_block_producer_likes_number = json.loads(
            BlockProducerLikeNumberDto.schema().dumps(block_producer_likes_number, many=True),
        )

        return JsonResponse({'result': serialized_block_producer_likes_number}, status=HTTPStatus.OK)
