"""
Provide configuration for admin panel block producer tables.
"""
from django.contrib import admin

from block_producer.models import (
    BlockProducer,
    BlockProducerLike,
)

admin.site.register(BlockProducer)
admin.site.register(BlockProducerLike)
