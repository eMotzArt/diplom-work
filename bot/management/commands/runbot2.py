import datetime
import random
import string

from django.core.management.base import BaseCommand

from bot.models import TgUser, TgState
from bot.tg.client import TgClient
from goals.models import Goal, Category


class Command(BaseCommand):
    def _get_random_string(self, length):
        letters = string.ascii_lowercase
        code = ''.join(random.choice(letters) for i in range(length))
        return code

    def _get_user_goals(self, user):
        user_goals = Goal.objects.filter(user=user).all()
        goals_list = [f"#{goal.id} {goal.title}" for goal in user_goals]
        return "\n".join(goals_list)

    def _get_user_state(self, user):
        state, created = TgState.objects.get_or_create(tg_user=user)
        return state

    def _get_user_step(self, user):
        state = self._get_user_state(user)
        return state.step

    def _set_user_step(self, user, step):
        TgState.objects.filter(tg_user=user).update(step=step)

    def _set_user_title(self, user, title):
        TgState.objects.filter(tg_user=user).update(title=title)

    def _set_user_category(self, user, category):
        TgState.objects.filter(tg_user=user).update(category=category)

    def _get_user_categories(self, user):
        user_categories = Category.objects.filter(user=user.app_user).all()
        categories_list = [f"#{cat.id} {cat.title}" for cat in user_categories]
        return "\n".join(categories_list)

    def _get_category_by_num_or_title(self, user, answer):
        if answer.isnumeric():
            if Category.objects.filter(user=user.app_user, pk=int(answer)).exists():
                return Category.objects.filter(user=user.app_user, pk=int(answer)).first()
            return None

        if Category.objects.filter(user=user.app_user, title=answer).exists():
            return Category.objects.filter(user=user.app_user, title=answer).first()
        return None

    def _clean_state(self, user):
        state = self._get_user_state(user)
        state.delete()

    def _create_goal(self, user):
        state = self._get_user_state(user)
        created_goal = Goal.objects.create(user=user.app_user,
                            title=state.title,
                            category=state.category,
                            due_date=datetime.date.today())
        return created_goal


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



                user_step = self._get_user_step(user)

                if user_step != 0 and message_text == '/cancel':
                    self._clean_state(user)
                    tg_client.send_message(chat_id, 'Goal creation cancelled')
                    continue


                if user_step == 0:
                    if message_text == '/goals':
                        goals = self._get_user_goals(user.app_user)
                        tg_client.send_message(chat_id, goals)
                        continue

                    if message_text == '/start':
                        tg_client.send_message(chat_id, "You can user /goals or /create commands")
                        continue

                    if message_text == '/create':
                        self._set_user_step(user, 1)
                        user_step = 1
                    else:
                        tg_client.send_message(chat_id, f"Wrong command.\nAvailable commands:\n/goals \n/create")
                        continue


                if user_step == 1:
                    if category := self._get_category_by_num_or_title(user, message_text):
                        tg_client.send_message(chat_id, f"Write goal title")
                        self._set_user_step(user, 2)
                        self._set_user_category(user, category)

                    else:
                        tg_client.send_message(chat_id, f"Which category do you want to select?\n"
                                                        f"Send category number or title\n"
                                                        f"{self._get_user_categories(user)}")
                    continue


                if user_step == 2:
                    if len(message_text)<=100:
                        self._set_user_title(user, message_text)
                        self._set_user_step(user, 3)
                        user_step = 3
                    else:
                        tg_client.send_message(chat_id, f"ERROR\n"
                                                        f"Maximum length: 100\n"
                                                        f"Write title again")
                        continue

                if user_step == 3:
                    created_goal = self._create_goal(user)
                    self._clean_state(user)
                    tg_client.send_message(chat_id, f"Goal successfully created\n"
                                                    f"#{created_goal.id} {created_goal.title}")


















