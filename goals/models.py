from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()

# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        abstract = True

class Board(BaseModel):
    title = models.CharField(max_length=50, blank=False, verbose_name='Название')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    def __str__(self):
        return self.title


class Category(BaseModel):
    title = models.CharField(max_length=50, verbose_name="Название")
    user = models.ForeignKey(USER, on_delete=models.CASCADE, verbose_name="Автор")
    is_deleted = models.BooleanField(default=False)
    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Goal(BaseModel):
    TODO = 1
    INWORK = 2
    COMPLETED = 3
    ARCHIVED = 4
    STATUSES = [
        (TODO, 'Goal for future'),
        (INWORK, 'Goal is  in work'),
        (COMPLETED, 'Goal is completed'),
        (ARCHIVED, 'Goal is archived'),
    ]

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    PRIORITY = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (CRITICAL, 'Critical')
    ]

    user = models.ForeignKey(USER, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey('goals.Category', blank=False, on_delete=models.CASCADE, related_name='goals', verbose_name='Категория')
    title = models.CharField(max_length=100, blank=False, verbose_name='Название')
    description = models.CharField(max_length=1000, verbose_name='Описание')
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=TODO, verbose_name='Статус')
    priority = models.PositiveSmallIntegerField(choices=PRIORITY, default=LOW, verbose_name='Приоритет')
    due_date = models.DateField(verbose_name='Дедлайн')

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self):
        return self.title

class Comment(BaseModel):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, verbose_name='Автор')
    goal = models.ForeignKey('goals.Goal', on_delete=models.CASCADE, verbose_name='Цель')
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class BoardParticipant(BaseModel):
    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(Board, on_delete=models.PROTECT, related_name="participants", verbose_name='Доска')
    user = models.ForeignKey(USER, on_delete=models.PROTECT, related_name="participants", verbose_name='Участник')
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.owner, verbose_name="Роль")

    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

