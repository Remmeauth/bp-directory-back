"""
Provide implementation of single block producer endpoint.
"""
import json
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from block_producer.domain.errors import BlockProducerWithSpecifiedIdentifierDoesNotExistError
from block_producer.domain.objects import (
    CreateBlockProducer,
    GetBlockProducer,
    GetBlockProducers,
    UpdateBlockProducer,
)
from block_producer.dto.block_producer import BlockProducerDto
from block_producer.forms import (
    CreateBlockProducerForm,
    UpdateBlockProducerForm,
)
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

        try:
            CreateBlockProducer(user=self.user, block_producer=self.block_producer).do(
                user_email=email, info=form.cleaned_data,
            )

        except UserWithSpecifiedEmailAddressDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'Block producer has been created.'}, status=HTTPStatus.OK)

    def post(self, request):
        """
        Update block producer.
        """
        user_email = request.user.email

        form = UpdateBlockProducerForm(request.data)

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        non_empty_request_data = {key: form.cleaned_data[key] for key in request.data}

        try:
            UpdateBlockProducer(
                user=self.user, block_producer=self.block_producer,
            ).do(user_email=user_email, info=non_empty_request_data)

        except UserWithSpecifiedEmailAddressDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'Block producer has been updated.'}, status=HTTPStatus.OK)


class GetBlockProducerSingle(APIView):
    """
    Single get block producer endpoint implementation.
    """

    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        """
        Constructor.
        """
        self.block_producer = BlockProducer()

    def get(self, request, block_producer_id):
        """
        Get block producer.
        """
        try:
            block_producer = GetBlockProducer(
                block_producer=self.block_producer,
            ).do(block_producer_id=block_producer_id)

        except BlockProducerWithSpecifiedIdentifierDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        serialized_block_producer = block_producer.to_dict()

        return JsonResponse({'result': serialized_block_producer}, status=HTTPStatus.OK)


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
