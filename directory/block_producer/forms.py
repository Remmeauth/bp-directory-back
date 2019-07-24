"""
Provide implementation of operation with block producer forms.
"""
from django import forms


class CommentBlockProducerForm(forms.Form):
    """
    Comment a block producer form implementation.
    """

    text = forms.CharField(max_length=200)
