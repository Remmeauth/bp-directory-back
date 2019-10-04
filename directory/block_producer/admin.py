"""
Provide configuration for admin panel block producer tables.
"""
from django.contrib import admin
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter

from block_producer.models import (
    BLOCK_PRODUCER_STATUSES,
    BlockProducer,
    BlockProducerComment,
    BlockProducerLike,
)


class BlockProducerStatusListFilter(MultipleChoiceListFilter):
    """
    Block producer model admin status field list filter.
    """
    title = 'Status'
    parameter_name = 'status__in'

    def lookups(self, request, model_admin):
        """
        Return lookups.
        """
        return BLOCK_PRODUCER_STATUSES


class BlockProducerAdmin(admin.ModelAdmin):
    """
    Block producer model admin.
    """

    list_display = ('user', 'name', 'status')
    list_filter = (BlockProducerStatusListFilter,)


admin.site.register(BlockProducer, BlockProducerAdmin)
admin.site.register(BlockProducerComment)
admin.site.register(BlockProducerLike)
