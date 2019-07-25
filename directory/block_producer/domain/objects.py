"""
Provide implementation of block producer domain.
"""
from block_producer.domain.errors import BlockProducerWithSpecifiedIdentifierDoesNotExistError
from user.domain.errors import UserWithSpecifiedEmailAddressDoesNotExistError


class CreateBlockProducer:
    """
    Create block producer implementation.
    """

    def __init__(self, user, block_producer):
        """
        Constructor.
        """
        self.user = user
        self.block_producer = block_producer

    def do(self, user_email, info):
        """
        Create a block producer.
        """
        if not self.user.does_exist(email=user_email):
            raise UserWithSpecifiedEmailAddressDoesNotExistError

        self.block_producer.create(email=user_email, info=info)


class UpdateBlockProducer:
    """
    Update block producer implementation.
    """

    def __init__(self, user, block_producer):
        """
        Constructor.
        """
        self.user = user
        self.block_producer = block_producer

    def do(self, user_email, info):
        """
        Update block producer.
        """
        if not self.user.does_exist(email=user_email):
            raise UserWithSpecifiedEmailAddressDoesNotExistError

        self.block_producer.update(email=user_email, info=info)


class LikeBlockProducer:
    """
    Liking block producer implementation.
    """

    def __init__(self, user, block_producer, block_producer_like):
        """
        Constructor.
        """
        self.user = user
        self.block_producer = block_producer
        self.block_producer_like = block_producer_like

    def do(self, user_email, block_producer_id):
        """
        To like a block producer.
        """
        if not self.user.does_exist(email=user_email):
            raise UserWithSpecifiedEmailAddressDoesNotExistError

        if not self.block_producer.does_exist(identifier=block_producer_id):
            raise BlockProducerWithSpecifiedIdentifierDoesNotExistError

        if self.block_producer_like.does_exist(user_email=user_email, block_producer_id=block_producer_id):
            self.block_producer_like.remove(user_email=user_email, block_producer_id=block_producer_id)

        else:
            self.block_producer_like.put(user_email=user_email, block_producer_id=block_producer_id)


class CommentBlockProducer:
    """
    Commenting block producer implementation.
    """

    def __init__(self, user, block_producer, block_producer_comment):
        """
        Constructor.
        """
        self.user = user
        self.block_producer = block_producer
        self.block_producer_comment = block_producer_comment

    def do(self, user_email, block_producer_id, text):
        """
        To comment a block producer.
        """
        if not self.user.does_exist(email=user_email):
            raise UserWithSpecifiedEmailAddressDoesNotExistError

        if not self.block_producer.does_exist(identifier=block_producer_id):
            raise BlockProducerWithSpecifiedIdentifierDoesNotExistError

        self.block_producer_comment.create(user_email=user_email, block_producer_id=block_producer_id, text=text)


class GetBlockProducers:
    """
    Get block producers implementation.
    """

    def __init__(self, block_producer):
        """
        Constructor.
        """
        self.block_producer = block_producer

    def do(self):
        """
        Get block producers.
        """
        return self.block_producer.get_all()
