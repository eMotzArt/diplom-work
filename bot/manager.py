import datetime
import random
import string

from bot.models import TgUser, TgState
from bot.tg.client import TgClient
from bot.tg.dc import GetUpdatesResponse
from goals.models import Goal, Category


class BotManager:
    user_id: int
    chat_id: int
    message: str
    current_user: TgUser
    current_state: TgState
    response: GetUpdatesResponse
    current_step: int | None


    def __init__(self):
        self.tg_client = TgClient()
        self.offset = 0

    def get_updates(self):
        self.response = self.tg_client.get_updates(offset=self.offset)

    def get_offset(self):
        return self.offset

    def user_exists(self):
        return TgUser.objects.filter(tg_user_id=self.user_id, tg_chat_id=self.chat_id).exists()

    def get_user(self):
        user, _ = TgUser.objects.get_or_create(tg_user_id=self.user_id, tg_chat_id=self.chat_id)
        return user

    def _get_random_code(self, length):
        letters = string.ascii_lowercase
        code = ''.join(random.choice(letters) for i in range(length))
        return code

    def verificate_user(self):
        verification_code = self._get_random_code(20)
        self.current_user.verification_code = verification_code
        self.current_user.save()
        self.tg_client.send_message(self.chat_id, f"Your verification code is: [{verification_code}]\n"
                                        f"Please put the verification code in to web-site")
    def is_app_user(self):
        return bool(self.current_user.app_user)

    def get_user_state(self):
        state, _ = TgState.objects.get_or_create(tg_user=self.current_user)
        self.current_state = state

    def get_user_step(self):
        self.current_step = self.current_state.step

    def clean_state(self):
        self.current_state.step = 0
        self.current_state.save()

    def get_user_goals(self):
        user_goals = Goal.objects.filter(user=self.current_user.app_user).all()
        goals_list = [f"#{goal.id} {goal.title}" for goal in user_goals]
        return "\n".join(goals_list)

    def get_user_categories(self):
        user_categories = Category.objects.filter(user=self.current_user.app_user).all()
        categories_list = [f"#{cat.id} {cat.title}" for cat in user_categories]
        return "\n".join(categories_list)

    def set_user_step(self, step):
        self.current_state.step = step
        self.current_state.save()
        self.current_step = step

    def get_category_by_num_or_title(self):
        if self.message.isnumeric():
            if Category.objects.filter(user=self.current_user.app_user, pk=int(self.message)).exists():
                return Category.objects.filter(user=self.current_user.app_user, pk=int(self.message)).first()
            return None

        if Category.objects.filter(user=self.current_user.app_user, title=self.message).exists():
            return Category.objects.filter(user=self.current_user.app_user, title=self.message).first()
        return None

    def set_user_category(self, category):
        TgState.objects.filter(tg_user=self.current_user).update(category=category)

    def set_user_title(self):
        self.current_state.title = self.message
        self.current_state.save()

    def create_goal(self):
        created_goal = Goal.objects.create(user=self.current_user.app_user,
                                           title=self.current_state.title,
                                           category=self.current_state.category,
                                           due_date=datetime.date.today())
        return created_goal

    def step_zero(self):
        if self.message == '/create':
            self.set_user_step(1)
            self.tg_client.send_message(self.chat_id, f"Which category do you want to select?\n"
                                                      f"Send category number or title\n"
                                                      f"{self.get_user_categories()}")
            return

        if self.message == '/goals':
            goals = self.get_user_goals()
            self.tg_client.send_message(self.chat_id, goals)
        elif self.message == '/start':
            self.tg_client.send_message(self.chat_id, "You can user /goals or /create commands")
        else:
            self.tg_client.send_message(self.chat_id, f"Wrong command.\nAvailable commands:\n/goals \n/create")

    def step_one(self):
        if category := self.get_category_by_num_or_title():
            self.tg_client.send_message(self.chat_id, f"Write goal title")
            self.set_user_step(2)
            self.set_user_category(category)
            return

        self.tg_client.send_message(self.chat_id, f"Which category do you want to select?\n"
                                        f"Send category number or title\n"
                                        f"{self.get_user_categories()}")

    def step_two(self):
        if len(self.message) <= 100:
            self.set_user_title()
            self.set_user_step(3)
            return True

        self.tg_client.send_message(self.chat_id, f"ERROR\n"
                                        f"Maximum length: 100\n"
                                        f"Write title again")

    def step_three(self):
        created_goal = self.create_goal()
        self.clean_state()
        self.tg_client.send_message(self.chat_id, f"Goal successfully created\n"
                                        f"#{created_goal.id} {created_goal.title}")

    def proceed_by_steps(self):
        self.get_user_state()
        self.get_user_step()

        if self.current_step != 0 and self.message == '/cancel':
            self.clean_state()
            self.tg_client.send_message(self.chat_id, 'Goal creation cancelled')
            return

        if self.current_step == 0:
            self.step_zero()
            return

        if self.current_step == 1:
            self.step_one()
            return

        if self.current_step == 2:
            is_ready_to_create = self.step_two()

            if is_ready_to_create:
                self.step_three()



    def process_response(self):
        for item in self.response.result:

            self.offset = item.update_id + 1
            self.chat_id = item.message.chat.id
            self.user_id = item.message.from_.id
            self.message = item.message.text

            if not self.user_exists() and self.message != '/start':
                # send instruction or do nothing (quiet mode)
                continue

            # if start was detected or user exists
            self.current_user = self.get_user()

            if not self.is_app_user():
                self.verificate_user()
                continue

            self.proceed_by_steps()
