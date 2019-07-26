"""
Provide implementation of block producer endpoints.
"""
from django.urls import path

from block_producer.views.block_producer import (
    BlockProducerCollection,
    BlockProducerSingle,
    GetBlockProducerSingle,
)
from block_producer.views.comment import BlockProducerCommentSingle
from block_producer.views.like import BlockProducerLikeSingle

block_producer_endpoints = [
    path('', BlockProducerSingle.as_view()),
    path('single/<int:block_producer_id>/', GetBlockProducerSingle.as_view()),
    path('collection/', BlockProducerCollection.as_view()),
    path('<int:block_producer_id>/comment/', BlockProducerCommentSingle.as_view()),
    path('<int:block_producer_id>/like/', BlockProducerLikeSingle.as_view()),
]
