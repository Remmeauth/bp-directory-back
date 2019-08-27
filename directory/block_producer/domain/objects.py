"""
Provide implementation of block producer domain.
"""
from block_producer.domain.errors import (
    BlockProducerDoesNotExistForSpecifiedUsername,
    BlockProducerWithSpecifiedIdentifierDoesNotExistError,
)
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
        if not self.user.does_exist_by_email(email=user_email):
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

    def do(self, user_email, block_producer_id, info):
        """
        Update block producer.
        """
        if not self.user.does_exist_by_email(email=user_email):
            raise UserWithSpecifiedEmailAddressDoesNotExistError

        self.block_producer.update(email=user_email, identifier=block_producer_id, info=info)


class GetBlockProducer:
    """
    Get block producer implementation.
    """

    def __init__(self, block_producer):
        """
        Constructor.
        """
        self.block_producer = block_producer

    def do(self, block_producer_id):
        """
        Get block producer by its identifier.
        """
        if not self.block_producer.does_exist(identifier=block_producer_id):
            raise BlockProducerWithSpecifiedIdentifierDoesNotExistError

        return self.block_producer.get(identifier=block_producer_id)


class GetUserLastBlockProducer:
    """
    Get user's last block producer implementation.
    """

    def __init__(self, block_producer):
        """
        Constructor.
        """
        self.block_producer = block_producer

    def do(self, user_email):
        """
        Get user's last block producer by username.
        """
        last_block_producer = self.block_producer.get_last(user_email=user_email)

        if last_block_producer is None:
            raise BlockProducerDoesNotExistForSpecifiedUsername

        return last_block_producer


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


class SearchBlockProducer:
    """
    Search block producers implementation.
    """

    def __init__(self, block_producer):
        """
        Constructor.
        """
        self.block_producer = block_producer

    def do(self, phrase):
        """
        Search block producers by phrase.
        """
        return self.block_producer.search(phrase=phrase)
