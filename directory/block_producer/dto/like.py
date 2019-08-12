"""
Provide implementation of block producer's like data transfer object.
"""
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from user.dto.user import UserDto


@dataclass_json
@dataclass
class BlockProducerLikeDto:
    """
    Block producer like data transfer object implementation.
    """

    id: int
    user_id: int
    block_producer_id: int

    user: UserDto
