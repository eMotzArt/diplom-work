import random
import string

from django.db import models
from django.contrib.auth import get_user_model

from goals.models import Category

USER = get_user_model()
# Create your models here.

class TgUser(models.Model):
    tg_chat_id = models.IntegerField()
    tg_user_id = models.IntegerField()
    verification_code = models.CharField(max_length=30, blank=True)
    app_user = models.ForeignKey(USER, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ['tg_user_id', 'tg_chat_id']
        verbose_name = "Бот->Пользователь"
        verbose_name_plural = "Бот->Пользователи"

    def _get_random_string(self):
        length = 10
        letters = string.ascii_lowercase
        code = ''.join(random.choice(letters) for i in range(length))
        return code

    def get_verification_code(self):
        verification_code = self._get_random_string()
        self.verification_code = verification_code
        self.save()
        return verification_code

class TgState(models.Model):
    class Step(models.IntegerChoices):
        non_procedure = 0, "Вне процедуры создания"
        not_selected = 1, "Выбор не выполнен"
        cat_selected = 2, "Категория выбрана"
        title_selected = 3, "Заголовок выбран"

    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE, null=False, blank=False)
    step = models.PositiveSmallIntegerField(choices=Step.choices, default=Step.non_procedure)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)

    def clean_state(self):
        self.step = 0
        self.save()

    def set_step(self, step):
        self.step = step
        self.save()

    def set_title(self, title):
        self.title = title
        self.save()

