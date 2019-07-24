"""
Provide implementation of block producer endpoints.
"""
from django.urls import path

from block_producer.views.block_producer import BlockProducerSingle
from block_producer.views.like import BlockProducerLikeSingle

block_producer_endpoints = [
    path('', BlockProducerSingle.as_view()),
    path('<int:block_producer_id>/like/', BlockProducerLikeSingle.as_view()),
]
