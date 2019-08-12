"""
Provide implementation of single block producer comment endpoint.
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
    CommentBlockProducer,
    GetBlockProducerComments,
)
from block_producer.forms import CommentBlockProducerForm
from block_producer.dto.comment import BlockProducerCommentDto
from block_producer.models import (
    BlockProducer,
    BlockProducerComment,
)
from user.domain.errors import UserWithSpecifiedEmailAddressDoesNotExistError
from user.models import User


class BlockProducerCommentCollection(APIView):
    """
    Collection block producer comment endpoint implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.block_producer = BlockProducer()
        self.block_producer_comment = BlockProducerComment()

    @authentication_classes((JSONWebTokenAuthentication, ))
    def put(self, request, block_producer_id):
        """
        To comment the block producer.
        """
        email = request.user.email
        text = request.data.get('text')

        form = CommentBlockProducerForm({
            'text': text,
        })

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        try:
            CommentBlockProducer(
                user=self.user, block_producer=self.block_producer, block_producer_comment=self.block_producer_comment,
            ).do(
                user_email=email, block_producer_id=block_producer_id, text=text,
            )
        except (
            BlockProducerWithSpecifiedIdentifierDoesNotExistError,
            UserWithSpecifiedEmailAddressDoesNotExistError,
        ) as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.NOT_FOUND)

        return JsonResponse({'result': 'Block producer has been commented.'}, status=HTTPStatus.OK)

    @permission_classes((permissions.AllowAny,))
    def get(self, request, block_producer_id):
        """
        Get block producer's comments.
        """
        block_producer_comments = GetBlockProducerComments(
            block_producer=self.block_producer,
            block_producer_comment=self.block_producer_comment,
        ).do(block_producer_id=block_producer_id)

        serialized_block_producer_comments = json.loads(
            BlockProducerCommentDto.schema().dumps(block_producer_comments, many=True),
        )

        return JsonResponse({'result': serialized_block_producer_comments}, status=HTTPStatus.OK)
