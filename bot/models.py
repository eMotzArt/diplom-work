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
        verbose_name = "Бот->Пользователь"
        verbose_name_plural = "Бот->Пользователи"
