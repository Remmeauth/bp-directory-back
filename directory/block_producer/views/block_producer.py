"""
Provide implementation of single block producer endpoint.
"""
import json
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from block_producer.domain.objects import (
    CreateBlockProducer,
    GetBlockProducers,
)
from block_producer.dto.block_producer import BlockProducerDto
from block_producer.forms import CreateBlockProducerForm
from block_producer.models import BlockProducer
from user.domain.errors import UserWithSpecifiedEmailAddressDoesNotExistError
from user.models import User


class BlockProducerSingle(APIView):
    """
    Single block producer endpoint implementation.
    """

    authentication_classes = (JSONWebTokenAuthentication,)

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.block_producer = BlockProducer()

    def put(self, request):
        """
        Create a block producer.
        """
        email = request.user.email

        form = CreateBlockProducerForm(data=request.data)

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)
        print(form.cleaned_data)
        try:
            CreateBlockProducer(user=self.user, block_producer=self.block_producer).do(
                user_email=email,
                info=form.cleaned_data,
            )

        except UserWithSpecifiedEmailAddressDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'Block producer has been created.'}, status=HTTPStatus.OK)


class BlockProducerCollection(APIView):
    """
    Collection block producer endpoint implementation.
    """

    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        """
        Constructor.
        """
        self.block_producer = BlockProducer()

    def get(self, request):
        """
        Get block producers.
        """
        block_producers = GetBlockProducers(block_producer=self.block_producer).do()
        serialized_block_producers = json.loads(BlockProducerDto.schema().dumps(block_producers, many=True))

        return JsonResponse({'result': serialized_block_producers}, status=HTTPStatus.OK)
