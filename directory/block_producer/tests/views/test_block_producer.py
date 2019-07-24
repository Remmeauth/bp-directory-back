"""
Provide tests for implementation of single block producer endpoint.
"""
import json
from http import HTTPStatus

from django.test import TestCase

from block_producer.models import BlockProducer
from user.models import User


class TestBlockProducerSingle(TestCase):
    """
    Implements tests for implementation of single block producer endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        self.user = User.objects.create_user(email='martin.fowler@gmail.com', password='martin.fowler.1337')

        response = self.client.post('/authentication/token/obtaining/', json.dumps({
            'email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        self.block_produce_info = {
            "name": "Block producer USA",
            "website_url": "https://bpusa.com",
            "location": "San Francisco, USA",
            "short_description": "Leading Block Producer - founded by a team of "
                                 "serial tech entrepreneurs, headquartered in USA",
            "full_description": "# About Us\n\nFounded by a team of serial tech entrepreneurs, "
                                "block producer USA is headquartered in San Francisco, USA and "
                                "is backed by reputable American financial players. We believe "
                                "that BP.IO will fundamentally change our economic and social "
                                "systems and as such we are deeply committed to contribute to "
                                "the growth of the ecosystem.",
            "logo_url": "",
            "linkedin_url": "https://www.linkedin.com/in/bpusa",
            "twitter_url": "https://twitter.com/bpusa",
            "medium_url": "https://medium.com/@bpusa",
            "github_url": "https://github.com/bpusa",
            "facebook_url": "https://www.facebook.com/bpusa",
            "telegram_url": "https://t.me/bpusa",
            "reddit_url": "https://reddit.com/@bpusa",
            "slack_url": "https://slack.com/bpusa",
            "wikipedia_url": "https://wikipedia.com/bpusa",
            "steemit_url": "https://steemit.com/@bpusa",
        }

        self.user_token = response.data.get('token')

    def test_create_block_producer(self):
        """
        Case: create block producer with specified information.
        Expect: block producer created in the database.
        """
        expected_result = {
            'result': 'Block producer has been created.',
        }

        response = self.client.put(
            f'/block-producers/',
            json.dumps(self.block_produce_info),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert BlockProducer.objects.get(user=self.user).name == 'Block producer USA'
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_create_block_producer_without_mandatory_argument(self):
        """
        Case: create block producer without mandatory argument.
        Expect: block producer created in the database.
        """
        expected_result = {
            'errors': {
                'name': ['This field is required.'],
            },
        }

        del self.block_produce_info['name']

        response = self.client.put(
            f'/block-producers/',
            json.dumps(self.block_produce_info),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code
