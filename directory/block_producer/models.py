"""
Provide database models for block producer.
"""
from django.conf import settings
from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
)
from django.db import models
from django.db.models import Count

from block_producer.dto.block_producer import BlockProducerDto
from block_producer.dto.comment import (
    BlockProducerCommentDto,
    BlockProducerCommentNumberDto,
)
from block_producer.dto.like import (
    BlockProducerLikeDto,
    BlockProducerLikeNumberDto,
)
from user.models import (
    User,
    Profile,
)

BLOCK_PRODUCER_STATUS_MODERATION = 'moderation'
BLOCK_PRODUCER_STATUS_DECLINED = 'declined'
BLOCK_PRODUCER_STATUS_ACTIVE = 'active'

BLOCK_PRODUCER_STATUSES = (
    (BLOCK_PRODUCER_STATUS_MODERATION, BLOCK_PRODUCER_STATUS_MODERATION),
    (BLOCK_PRODUCER_STATUS_DECLINED, BLOCK_PRODUCER_STATUS_DECLINED),
    (BLOCK_PRODUCER_STATUS_ACTIVE, BLOCK_PRODUCER_STATUS_ACTIVE),
)


class BlockProducer(models.Model):
    """
    Block producer database model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, blank=False)
    website_url = models.URLField(max_length=200, blank=False)
    location = models.CharField(max_length=100, blank=True)
    short_description = models.CharField(max_length=100, blank=False)
    full_description = models.TextField(max_length=10000, blank=True)
    logo_url = models.URLField(max_length=1000, blank=True, default=settings.DEFAULT_BLOCK_PRODUCER_LOGOTYPE_URL)

    status = models.CharField(max_length=10, choices=BLOCK_PRODUCER_STATUSES, default=BLOCK_PRODUCER_STATUS_MODERATION)
    status_description = models.TextField(max_length=10000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    linkedin_url = models.URLField(max_length=200, blank=True)
    twitter_url = models.URLField(max_length=200, blank=True)
    medium_url = models.URLField(max_length=200, blank=True)
    github_url = models.URLField(max_length=200, blank=True)
    facebook_url = models.URLField(max_length=200, blank=True)
    telegram_url = models.URLField(max_length=200, blank=True)
    reddit_url = models.URLField(max_length=200, blank=True)
    slack_url = models.URLField(max_length=200, blank=True)
    wikipedia_url = models.URLField(max_length=200, blank=True)
    steemit_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        """
        Get string representation of an object.
        """
        return f'{self.name} — {self.user.email}'

    @classmethod
    def does_exist(cls, identifier):
        """
        Check if block producer exists by its identifier.
        """
        if cls.objects.filter(id=identifier).exists():
            return True

        return False

    @classmethod
    def get_all(cls):
        """
        Get block producers.
        """
        block_producers_as_dicts = cls.objects.all().order_by('-created_at').values()

        for block_producer in block_producers_as_dicts:

            user_identifier = block_producer.get('user_id')
            user_as_dict = User.objects.filter(id=user_identifier).values().first()

            del user_as_dict['password']
            del user_as_dict['created']

            block_producer['user'] = user_as_dict
            del block_producer['created_at']

        return BlockProducerDto.schema().load(block_producers_as_dicts, many=True)

    @classmethod
    def create(cls, email, info):
        """
        Create a block producer with specified information.
        """
        user = User.objects.get(email=email)

        if not info.get('logo_url'):
            del info['logo_url']

        cls.objects.create(user=user, **info)

    @classmethod
    def update(cls, email, identifier, info):
        """
        Update block producer with specified information.
        """
        user = User.objects.get(email=email)
        cls.objects.filter(user=user, id=identifier).update(**info)

    @classmethod
    def get(cls, identifier):
        """
        Get block producer by its identifier.
        """
        block_producer_as_dict = cls.objects.filter(id=identifier).values().first()

        user_identifier = block_producer_as_dict.get('user_id')
        user_as_dict = User.objects.filter(id=user_identifier).values().first()

        del user_as_dict['password']
        del user_as_dict['created']

        block_producer_as_dict['user'] = user_as_dict
        del block_producer_as_dict['created_at']

        return BlockProducerDto(**block_producer_as_dict)

    @classmethod
    def search(cls, phrase):
        """
        Search block producers by phrase.
        """
        search_vector = SearchVector('name', weight='A') + \
            SearchVector('location', weight='B') + \
            SearchVector('short_description', weight='B') + \
            SearchVector('full_description', weight='B')

        block_producers_as_list = cls.objects.annotate(
            search=search_vector,
        ).filter(search=SearchQuery(phrase)).order_by('-created_at').values()

        for block_producer_as_dict in block_producers_as_list:
            user_identifier = block_producer_as_dict.get('user_id')

            user_as_dict = User.objects.filter(id=user_identifier).values().first()

            del user_as_dict['password']
            del user_as_dict['created']

            del block_producer_as_dict['search']
            del block_producer_as_dict['created_at']

            block_producer_as_dict['user'] = user_as_dict

        return BlockProducerDto.schema().load(block_producers_as_list, many=True)

    @classmethod
    def get_last(cls, username):
        """
        Get user's last block producer by username.
        """
        block_producers_as_dict = cls.objects.filter(user__username=username)

        if not block_producers_as_dict:
            return None

        last_block_producer = block_producers_as_dict.values().last()

        user_identifier = last_block_producer.get('user_id')
        user_as_dict = User.objects.filter(id=user_identifier).values().first()

        del user_as_dict['password']
        del user_as_dict['created']

        last_block_producer['user'] = user_as_dict
        del last_block_producer['created_at']

        return BlockProducerDto(**last_block_producer)

    @classmethod
    def delete_(cls, identifier):
        """
        Delete block producer by its identifier.
        """
        cls.objects.filter(id=identifier).delete()

    @classmethod
    def get_status_description(cls, email, identifier):
        """
        Get block producer status description by its identifier.
        """
        block_producer_as_dict = cls.objects.filter(user__email=email, id=identifier).values().first()

        return block_producer_as_dict.get('status_description')


class BlockProducerLike(models.Model):
    """
    Block producer like database model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block_producer = models.ForeignKey(BlockProducer, on_delete=models.CASCADE)

    def __str__(self):
        """
        Get string representation of an object.
        """
        return f'{self.block_producer.name} — {self.user.email}'

    @classmethod
    def does_exist(cls, user_email, block_producer_id):
        """
        Check if block producer like exists by user e-mail address and block producer identifier.
        """
        user = User.objects.get(email=user_email)
        block_producer = BlockProducer.objects.get(id=block_producer_id)

        if cls.objects.filter(user=user, block_producer=block_producer).exists():
            return True

        return False

    @classmethod
    def put(cls, user_email, block_producer_id):
        """
        To like to block producer.
        """
        user = User.objects.get(email=user_email)
        block_producer = BlockProducer.objects.get(id=block_producer_id)

        cls.objects.create(user=user, block_producer=block_producer)

    @classmethod
    def remove(cls, user_email, block_producer_id):
        """
        To unlike to block producer.
        """
        user = User.objects.get(email=user_email)
        block_producer = BlockProducer.objects.get(id=block_producer_id)

        block_producer_like = cls.objects.get(user=user, block_producer=block_producer)
        block_producer_like.delete()

    @classmethod
    def get_all(cls, block_producer_id):
        """
        Get likes for block producer.
        """
        block_producer = BlockProducer.objects.get(id=block_producer_id)

        block_producer_likes_as_dicts = cls.objects.filter(block_producer=block_producer).values()

        for block_producer_like in block_producer_likes_as_dicts:
            user_identifier = block_producer_like.get('user_id')
            user_as_dict = User.objects.filter(id=user_identifier).values().first()

            del user_as_dict['password']
            del user_as_dict['created']

            block_producer_like['user'] = user_as_dict

        return BlockProducerLikeDto.schema().load(block_producer_likes_as_dicts, many=True)

    @classmethod
    def get_numbers(cls):
        """
        Get likes numbers for block producers.
        """
        block_producer_likes_numbers = cls.objects.all().values(
            'block_producer_id',
        ).annotate(likes=Count('id'))

        return BlockProducerLikeNumberDto.schema().load(block_producer_likes_numbers, many=True)


class BlockProducerComment(models.Model):
    """
    Block producer comment database model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block_producer = models.ForeignKey(BlockProducer, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Get string representation of an object.
        """
        return f'{self.block_producer.name} — {self.user.email} — {self.created_at}'

    @classmethod
    def create(cls, user_email, block_producer_id, text):
        """
        Create comment for block producer.
        """
        user = User.objects.get(email=user_email)
        block_producer = BlockProducer.objects.get(id=block_producer_id)

        cls.objects.create(user=user, block_producer=block_producer, text=text)

    @classmethod
    def get_all(cls, block_producer_id):
        """
        Get comments for block producer.
        """
        block_producer = BlockProducer.objects.get(id=block_producer_id)

        block_producer_comments_as_dicts = cls.objects.filter(block_producer=block_producer).values()

        for block_producer_comment in block_producer_comments_as_dicts:

            user_identifier = block_producer_comment.get('user_id')
            user_as_dict = User.objects.filter(id=user_identifier).values().first()

            profile = Profile.objects.get(user__id=user_identifier)

            del user_as_dict['password']
            del user_as_dict['created']

            block_producer_comment['user'] = user_as_dict
            block_producer_comment['profile_avatar_url'] = profile.avatar_url

        return BlockProducerCommentDto.schema().load(block_producer_comments_as_dicts, many=True)

    @classmethod
    def get_numbers(cls):
        """
        Get comments numbers for block producers.
        """
        block_producer_comments_numbers = cls.objects.all().values(
            'block_producer_id',
        ).annotate(comments=Count('text'))

        return BlockProducerCommentNumberDto.schema().load(block_producer_comments_numbers, many=True)
