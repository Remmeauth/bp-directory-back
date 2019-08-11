"""
Provide tests for implementation of single block producer comment endpoint.
"""
import json
from http import HTTPStatus

from django.test import TestCase

from block_producer.models import (
    BlockProducer,
    BlockProducerComment,
)
from user.models import User


class TestBlockProducerCommentSingle(TestCase):
    """
    Implements tests for implementation of single block producer comment endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        user = User.objects.create_user(
            email='martin.fowler@gmail.com',
            username='martin.fowler',
            password='martin.fowler.1337',
        )
        block_producer = BlockProducer.objects.create(
            user=user,
            name='Block producer Canada',
            website_url='https://bpcanada.com',
            short_description='Founded by a team of serial tech entrepreneurs in Canada.',
        )

        response = self.client.post('/authentication/token/obtaining/', json.dumps({
            'username_or_email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        self.user = user
        self.user_token = response.data.get('token')
        self.block_producer = block_producer

    def test_comment(self):
        """
        Case: to comment a block producer.
        Expect: block producer comment record is created in database.
        """
        expected_result = {
            'result': 'Block producer has been commented.',
        }

        response = self.client.put(
            f'/block-producers/{self.block_producer.id}/comments/',
            json.dumps({'text': 'Great block producer!'}),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert BlockProducerComment.objects.get(user=self.user, block_producer=self.block_producer)
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_comment_non_existing_block_producer(self):
        """
        Case: to comment a non-exiting block producer.
        Expect: block producer with specified identifier does not exist error message.
        """
        non_existing_block_producer_id = 100500

        expected_result = {
            'error': 'Block producer with specified identifier does not exist.',
        }

        response = self.client.put(
            f'/block-producers/{non_existing_block_producer_id}/comments/',
            json.dumps({'text': 'Great block producer!'}),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_comment_block_producer_without_data(self):
        """
        Case: to comment a block producer without text.
        Expect: text is required error message.
        """
        expected_result = {
            'errors': {
                'text': [
                    'This field is required.',
                ],
            },
        }

        response = self.client.put(
            f'/block-producers/{self.block_producer.id}/comments/',
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code

    def test_comment_block_producer_with_exceeded_text_length(self):
        """
        Case: to comment a non-exiting block producer with exceeded text length.
        Expect: ensure this value has at most then allowed characters error message.
        """
        expected_result = {
            'errors': {
                'text': [
                    'Ensure this value has at most 200 characters (it has 201).',
                ],
            },
        }

        response = self.client.put(
            f'/block-producers/{self.block_producer.id}/comments/',
            json.dumps({'text': 'T' * 201}),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code
