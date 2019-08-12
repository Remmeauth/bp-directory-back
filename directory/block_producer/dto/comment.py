"""
Provide implementation of block producer's comment data transfer object.
"""
import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from user.dto.user import UserDto


@dataclass_json
@dataclass
class BlockProducerCommentDto:
    """
    Block producer comment data transfer object implementation.
    """

    id: int
    user_id: int
    block_producer_id: int

    user: UserDto

    text: str
    created_at: typing.Any
