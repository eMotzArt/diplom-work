import requests
import os

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.token: str = os.getenv('BOT_TOKEN')
        self.link: str = f'https://api.telegram.org/bot{self.token}'


    def _get_url(self, method: str) -> str:
        """Метод возвращает ссылку для указанного метода

        """
        return f"{self.link}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """Функция метода: получит список новых сообщений от бота
        Метод отправляет запрос по ссылке, получает ответ, возвращает сформированный на основе ответа датакласс

        """
        response = requests.get(self._get_url('getUpdates'), params={'timeout': timeout, 'offset': offset})

        return GetUpdatesResponse.from_dict(response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """Функция метода: бот отправит сообщение пользователю
        Метод отправляет запрос по ссылке, получает ответ, возвращает сформированный на основе ответа датакласс

        """
        response = requests.get(self._get_url('sendMessage'), params={'chat_id': chat_id, 'text': text})
        return SendMessageResponse.from_dict(response.json())
