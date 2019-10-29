"""
Provide implementation of Telegram bot.
"""
import json

import requests
from django.conf import settings


class TelegramBot:
    """
    Telegram bot implementation.
    """

    def __init__(self, host=settings.TELEGRAM_BOT_HOST, token=settings.TELEGRAM_BOT_TOKEN):
        """
        Constructor.
        """
        self.token = token
        self.host = host

    def _send_message_telegram_api(self, chat_id, message):
        """
        Send request to Telegram API to send message from bot.
        """
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown',
        }

        requests.post(f'https://api.telegram.org/bot{self.token}/sendMessage', data=json.dumps(data), headers={
            'Content-type': 'application/json',
        })

    def notify_block_producer_creation(self, admin_host, block_producer_identifier):
        """
        Notify block producer creation.
        """
        subscribers = requests.get(f'{self.host}/subscribers/block-producer/creation', headers={
            'Content-type': 'application/json',
        }).json().get('result')

        administrators = requests.get(f'{self.host}/administrators', headers={
            'Content-type': 'application/json',
        }).json().get('result')

        link_to_moderate = f'{admin_host}/admin/block_producer/blockproducer/{block_producer_identifier}/change/'

        for subscriber in subscribers:
            message = f'Block producer with identifier {block_producer_identifier} has been created.'

            subscriber_chat_id = subscriber.get('chat_id')

            if subscriber in administrators:
                message += f'\nTo moderate use following [link]({link_to_moderate}).'

            self._send_message_telegram_api(chat_id=subscriber_chat_id, message=message)

    def notify_block_producer_update(self, admin_host, block_producer_identifier):
        """
        Notify block producer update.
        """
        subscribers = requests.get(f'{self.host}/subscribers/block-producer/creation', headers={
            'Content-type': 'application/json',
        }).json().get('result')

        administrators = requests.get(f'{self.host}/administrators', headers={
            'Content-type': 'application/json',
        }).json().get('result')

        link_to_moderate = f'{admin_host}/admin/block_producer/blockproducer/{block_producer_identifier}/change/'

        for subscriber in subscribers:
            message = f'Block producer with identifier {block_producer_identifier} has been updated.'

            subscriber_chat_id = subscriber.get('chat_id')

            if subscriber in administrators:
                message += f'\nTo moderate use following [link]({link_to_moderate}).'

            self._send_message_telegram_api(chat_id=subscriber_chat_id, message=message)
