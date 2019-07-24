"""
Provide implementation of single block producer comment endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from block_producer.domain.errors import BlockProducerWithSpecifiedIdentifierDoesNotExistError
from block_producer.domain.objects import CommentBlockProducer
from block_producer.forms import CommentBlockProducerForm
from block_producer.models import (
    BlockProducer,
    BlockProducerComment,
)
from user.domain.errors import UserWithSpecifiedEmailAddressDoesNotExistError
from user.models import User


class BlockProducerCommentSingle(APIView):
    """
    Single block producer comment endpoint implementation.
    """

    authentication_classes = (JSONWebTokenAuthentication,)

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.block_producer = BlockProducer()
        self.block_producer_comment = BlockProducerComment()

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
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'Block producer has been commented.'}, status=HTTPStatus.OK)
