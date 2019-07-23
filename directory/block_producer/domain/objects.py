"""
Provide implementation of block producer domain.
"""
from block_producer.domain.errors import BlockProducerWithSpecifiedIdentifierDoesNotExistError
from user.domain.errors import UserWithSpecifiedEmailAddressDoesNotExistError


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
