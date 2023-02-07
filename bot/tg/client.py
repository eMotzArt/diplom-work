import requests
import os

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.token = os.getenv('BOT_TOKEN')
        self.link = f'https://api.telegram.org/bot{self.token}'

    def _get_url(self, method: str):
        return f"{self.link}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        response = requests.get(self._get_url('getUpdates'), params={'timeout': timeout, 'offset': offset})

        return GetUpdatesResponse.from_dict(response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        response = requests.get(self._get_url('sendMessage'), params={'chat_id': chat_id, 'text': text})
        return SendMessageResponse.from_dict(response.json())
