import datetime

from bot.models import TgUser, TgState
from bot.tg.client import TgClient
from bot.tg.dc import GetUpdatesResponse, UpdateObj
from goals.models import Goal, Category


class BotManager:
    """Класс менеджера-бота, получающего и обрабатывающего новую информацию от бота и отправляющего ответы
    
    """
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

    def get_updates(self) -> None:
        """Метод для получения и сохранения в экземпляре всех новых сообщений с telegram-клиента

        """
        self.response = self.tg_client.get_updates(offset=self.offset)

    def get_offset(self) -> int:
        """Метод возвращающий текущий оффсет для последующего запроса на получение новых сообщений

        """
        return self.offset

    def user_exists(self) -> bool:
        """Метод проверяющий наличие в базе текущего пользователя по его id и id чата

        """
        return TgUser.objects.filter(tg_user_id=self.user_id, tg_chat_id=self.chat_id).exists()

    def get_user(self) -> TgUser:
        """Метод возвращающий (или создающий, в случае отсутствия) пользователя

        """
        user, _ = TgUser.objects.get_or_create(tg_user_id=self.user_id, tg_chat_id=self.chat_id)
        return user

    def verificate_user(self) -> None:
        """Метод записывает в базу сгенерированный случайный код для верификации и отправляет его пользователю

        """
        verification_code = self.current_user.get_verification_code()
        self.tg_client.send_message(self.chat_id, f"Your verification code is: [{verification_code}]\n"
                                        f"Please put the verification code in to web-site")

    def is_app_user(self) -> bool:
        """Метод проверяет привязан ли пользователь приложения к текущему телеграм-пользователю (идентифицирован ли он)

        """
        return bool(self.current_user.app_user)

    def get_user_state(self) -> None:
        """Метод созхраняет в экземпляр найденную или создает для пользователя TgState запись в БД
        (для отслеживания на каком этапе создания новой цели пользователь находится)

        """
        state, _ = TgState.objects.get_or_create(tg_user=self.current_user)
        self.current_state: TgState = state

    def get_user_step(self) -> None:
        """Метод возвращает текущий "этап" пользователя
        (0 - не создает, 1-2-3 - задает категорию-задает название цели-этап генерации новой цели)

        """
        self.current_step: int = self.current_state.step

    def get_user_goals(self) -> str:
        """Метод формирует и возвращает строку со списком целей пользователя или строку с ответом что их нет

        """
        accessed_categories = Category.objects.filter(board__participants__user=self.current_user.app_user,
                                                      is_deleted=False)
        user_goals = Goal.objects.filter(category__in=accessed_categories, status__in=[1, 2, 3]).all()

        if user_goals:
            goals_list = [f"#{goal.id} {goal.title}" for goal in user_goals]
            return "\n".join(goals_list)
        return "You have no goals"

    def get_user_categories(self) -> str:
        """Метод формирует и возвращает строку со списком категорий пользователя или строку с ответом что их нет

        """
        user_categories = Category.objects.filter(
            board__participants__user=self.current_user.app_user,
            board__participants__role__in=[1, 2],
            is_deleted=False
        )

        if user_categories:
            categories_list = [f"#{cat.id} {cat.title}" for cat in user_categories]
            return "\n".join(categories_list)

    def set_user_step(self, step: int):
        """Метод записывает в state пользователя его текущий шаг, а так же в экземпляр, для удобства доступа

        """
        self.current_state.set_step(step)
        self.current_step = step

    def get_category_by_num_or_title(self) -> Category:
        """Метод находит и возвращает категорию пользователя по номеру или названию

        """
        filters = {
            'board__participants__user': self.current_user.app_user,
            'is_deleted': False,
            'title': None if self.message.isnumeric() else self.message,
            'pk': None if not self.message.isnumeric() else int(self.message)
        }
        if self.message.isnumeric():
            filters.pop('title')
        else:
            filters.pop('pk')

        user_category = Category.objects.filter(**filters).first()
        return user_category

    def set_user_category(self, category: Category) -> None:
        """Метод записывает в state (состояние) пользователя категорию, к которой он хочет создать цель

        """
        TgState.objects.filter(tg_user=self.current_user).update(category=category)

    def create_goal(self) -> Goal:
        """Метод создает и возвращает цель

        """
        created_goal = Goal.objects.create(user=self.current_user.app_user,
                                           title=self.current_state.title,
                                           category=self.current_state.category,
                                           due_date=datetime.date.today())
        return created_goal

    def step_zero(self) -> None:
        """Метод проверяет какую комманду ввёл пользователь
        и в зависимости от этого пишет пользователю ответ с дальнейшими инструкциями

        """
        if self.message == '/create':
            user_categories = self.get_user_categories()
            if not user_categories:
                self.tg_client.send_message(self.chat_id, f"You have no categories")
                return
            self.set_user_step(1)
            self.tg_client.send_message(self.chat_id, f"Which category do you want to select?\n"
                                                      f"Send category number or title\n"
                                                      f"{user_categories}\n"
                                                      f"Also you can send /cancel to abort")
            return

        if self.message == '/goals':
            goals = self.get_user_goals()
            self.tg_client.send_message(self.chat_id, goals)

        elif self.message == '/start':
            self.tg_client.send_message(self.chat_id, "You can user /goals or /create commands")
        else:
            self.tg_client.send_message(self.chat_id, f"Wrong command.\nAvailable commands:\n/goals \n/create")

    def step_one(self) -> None:
        """Метод ищет категорию по номеру или названию (содержимое сообщение пользователя).
        В случае нахождения - повышает этап пользователя до 2
        Иначе повосторно отправляет запрос со списком категорий

        """
        if category := self.get_category_by_num_or_title():
            self.tg_client.send_message(self.chat_id, f"Write goal title to create or /cancel to abort")
            self.set_user_step(2)
            self.set_user_category(category)
            return

        self.tg_client.send_message(self.chat_id, f"Which category do you want to select?\n"
                                        f"Send category number or title\n"
                                        f"{self.get_user_categories()}\n"
                                        f"Also you can send /cancel to abort")

    def step_two(self) -> None | bool:
        """Метод записывает в state (состояние) title полученный отпользователя если его длина
        не превышает 100 символов (ограничение модели БД). Иначе возвращает пояснение
        с просит повторное введение title

        """
        if len(self.message) <= 100:
            self.current_state.set_title(self.message)
            self.set_user_step(3)
            return True

        self.tg_client.send_message(self.chat_id, f"ERROR\n"
                                        f"Maximum length: 100\n"
                                        f"Write title again")

    def step_three(self) -> None:
        """Метод создает цель, обнуляет state пользователя и отправляет сообщение об успехе с данными цели

        """
        created_goal = self.create_goal()
        self.current_state.clean_state()
        self.tg_client.send_message(self.chat_id, f"Goal successfully created\n"
                                        f"#{created_goal.id} {created_goal.title}")

    def proceed_by_steps(self) -> None:
        """Метод проводит пользователя в зависимости от его этапа по соответствующим методам
        Так же следит за сообщением /cancel для отмены процесса создания цели

        """
        self.get_user_state()
        self.get_user_step()

        if self.current_step != 0 and self.message == '/cancel':
            self.current_state.clean_state()
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

    def collect_data(self, message: UpdateObj) -> None:
        """Метод собирает в экземпляр необходимые для алгоритма данные

        """
        self.offset = message.update_id + 1
        self.chat_id = message.message.chat.id
        self.user_id = message.message.from_.id
        self.message = message.message.text

    def process_response(self) -> None:
        """Метод обрабатывает новые сообщения от пользователей, проверяет верифицирован ли пользователь,
        верифицирует в случае необходимости. После верификации запускает основной алгоритм работы с пользователем

        """
        for item in self.response.result:
            self.collect_data(item)

            if not self.user_exists() and self.message != '/start':
                # send instruction or do nothing (quiet mode)
                continue

            # if start was detected or user exists
            self.current_user = self.get_user()

            if not self.is_app_user():
                self.verificate_user()
                continue

            self.proceed_by_steps()
