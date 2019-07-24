"""
Provide implementation of single block producer endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from block_producer.domain.objects import BlockProducer
from block_producer.forms import CreateBlockProducerForm
from block_producer import models
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
        self.block_producer = models.BlockProducer()

    def put(self, request):
        """
        Create a block producer.
        """
        email = request.user.email

        name = request.data.get('name')
        website_url = request.data.get('website_url')
        location = request.data.get('location')
        short_description = request.data.get('short_description')
        full_description = request.data.get('full_description')
        logo_url = request.data.get('logo_url')
        linkedin_url = request.data.get('linkedin_url')
        twitter_url = request.data.get('twitter_url')
        medium_url = request.data.get('medium_url')
        github_url = request.data.get('github_url')
        facebook_url = request.data.get('facebook_url')
        telegram_url = request.data.get('telegram_url')
        reddit_url = request.data.get('reddit_url')
        slack_url = request.data.get('slack_url')
        wikipedia_url = request.data.get('wikipedia_url')
        steemit_url = request.data.get('steemit_url')

        info = {
            'name': name,
            'website_url': website_url,
            'location': location,
            'short_description': short_description,
            'full_description': full_description,
            'logo_url': logo_url,
            'linkedin_url': linkedin_url,
            'twitter_url': twitter_url,
            'medium_url': medium_url,
            'github_url': github_url,
            'facebook_url': facebook_url,
            'telegram_url': telegram_url,
            'reddit_url': reddit_url,
            'slack_url': slack_url,
            'wikipedia_url': wikipedia_url,
            'steemit_url': steemit_url,
        }

        form = CreateBlockProducerForm(data=info)

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        try:
            BlockProducer(user=self.user, block_producer=self.block_producer).do(user_email=email, info=info)

        except UserWithSpecifiedEmailAddressDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'Block producer card has been created.'}, status=HTTPStatus.OK)
