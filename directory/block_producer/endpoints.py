"""
Provide implementation of block producer endpoints.
"""
from django.urls import path

from block_producer.views.block_producer import (
    BlockProducerCollection,
    BlockProducerSearchCollection,
    BlockProducerSingle,
)
from block_producer.views.comment import BlockProducerCommentCollection
from block_producer.views.like import BlockProducerLikeSingle

block_producer_endpoints = [
    path('', BlockProducerCollection.as_view()),
    path('search/', BlockProducerSearchCollection.as_view()),
    path('<int:block_producer_id>/', BlockProducerSingle.as_view()),
    path('<int:block_producer_id>/comments/', BlockProducerCommentCollection.as_view()),
    path('<int:block_producer_id>/like/', BlockProducerLikeSingle.as_view()),
]
