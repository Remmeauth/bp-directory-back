"""
Provide implementation of block producer endpoints.
"""
from django.urls import path

from block_producer.views.block_producer import (
    BlockProducerCollection,
    BlockProducerSearchCollection,
    BlockProducerSingle,
)
from block_producer.views.comment import (
    BlockProducerCommentCollection,
    BlockProducerCommentNumberCollection,
)
from block_producer.views.like import (
    BlockProducerLikeCollection,
    BlockProducerLikeNumberCollection,
)

block_producer_endpoints = [
    path('', BlockProducerCollection.as_view()),
    path('search/', BlockProducerSearchCollection.as_view()),
    path('<int:block_producer_id>/', BlockProducerSingle.as_view()),
    path('<int:block_producer_id>/comments/', BlockProducerCommentCollection.as_view()),
    path('comments/numbers/', BlockProducerCommentNumberCollection.as_view()),
    path('likes/numbers/', BlockProducerLikeNumberCollection.as_view()),
    path('<int:block_producer_id>/likes/', BlockProducerLikeCollection.as_view()),
]
