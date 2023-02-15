from django.core.management.base import BaseCommand

from bot.manager import BotManager


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        bot_manager = BotManager()
        while True:
            bot_manager.get_updates()
            bot_manager.process_response()
