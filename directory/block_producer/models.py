"""
Provide database models for block producer.
"""
from django.db import models

from user.models import User


class BlockProducer(models.Model):
    """
    Block producer database model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, null=False, blank=False)
    website_url = models.URLField(max_length=200, null=False, blank=False)
    location = models.CharField(max_length=100, blank=True, null=True)
    short_description = models.CharField(max_length=100, null=False, blank=False)
    full_description = models.TextField(blank=True, null=True)
    logo_url = models.URLField(max_length=200, blank=True, null=True)

    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    medium_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)
    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    telegram_url = models.URLField(max_length=200, blank=True, null=True)
    reddit_url = models.URLField(max_length=200, blank=True, null=True)
    slack_url = models.URLField(max_length=200, blank=True, null=True)
    wikipedia_url = models.URLField(max_length=200, blank=True, null=True)
    steemit_url = models.URLField(max_length=200, blank=True, null=True)

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
    def create(cls, email, info):
        """
        Create a block producer with specified information.
        """
        user = User.objects.get(email=email)

        cls.objects.create(
            user=user,
            name=info.get('name'),
            website_url=info.get('website_url'),
            location=info.get('location'),
            short_description=info.get('short_description'),
            full_description=info.get('full_description', ''),
            logo_url=info.get('logo_url', ''),
            linkedin_url=info.get('linkedin_url', ''),
            twitter_url=info.get('twitter_url', ''),
            medium_url=info.get('medium_url', ''),
            github_url=info.get('github_url', ''),
            facebook_url=info.get('facebook_url', ''),
            telegram_url=info.get('telegram_url', ''),
            reddit_url=info.get('reddit_url', ''),
            slack_url=info.get('slack_url', ''),
            wikipedia_url=info.get('wikipedia_url', ''),
            steemit_url=info.get('steemit_url', ''),
        )


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


class BlockProducerComment(models.Model):
    """
    Block producer comment database model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block_producer = models.ForeignKey(BlockProducer, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=False)
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
