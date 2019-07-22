"""
Provide configuration for admin panel block producer tables.
"""
from django.contrib import admin

from block_producer.models import BlockProducer

admin.site.register(BlockProducer)
