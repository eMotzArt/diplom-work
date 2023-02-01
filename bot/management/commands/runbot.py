import random
import string

from django.core.management.base import BaseCommand
from django.core.management import call_command

from bot.models import TgUser
from bot.tg.client import TgClient
from goals.models import Goal


class Command(BaseCommand):
    def _get_random_string(self, length):
        letters = string.ascii_lowercase
        code = ''.join(random.choice(letters) for i in range(length))
        return code

    def _get_user_goals(self, user):
        user_goals = Goal.objects.filter(user=user).all()
        goals_list = [f"#{goal.id} {str(goal)}" for goal in user_goals]
        return "\n".join(goals_list)

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient()
        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1

                chat_id = item.message.chat.id
                user_id = item.message.from_.id
                message_text = item.message.text

                tg_user_exists = TgUser.objects.filter(tg_user_id=user_id, tg_chat_id=chat_id).exists()

                if not tg_user_exists and message_text != '/start':
                    # send instruction or do nothing (quiet mode)
                    continue



                # if start was detected or user exists
                user, created = TgUser.objects.get_or_create(tg_user_id=user_id, tg_chat_id=chat_id)

                if not user.app_user:
                    verification_code = self._get_random_string(20)
                    user.verification_code = verification_code
                    user.save()
                    tg_client.send_message(chat_id, f"Your verification code is: [{verification_code}]\n"
                                                    f"Please put the verification code in to web-site")
                    continue

                if message_text == '/goals':
                    goals = self._get_user_goals(user.app_user)
                    tg_client.send_message(chat_id, goals)
                    continue

                if message_text == '/create':
                    pass
                    continue

                if message_text == '/start':
                    tg_client.send_message(chat_id, "We're already started")
                    continue


                tg_client.send_message(chat_id, f"Wrong command.\nAvailable commands:\n/goals \n/create")



                # tg_client.send_message(chat_id, message_text)
