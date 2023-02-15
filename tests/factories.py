import factory, factory.django
from pytest_factoryboy import register

from core.models import User
from goals.models import BoardParticipant, Board, Category, Goal

TEST_USER_EMAIL = "test_user@email.ru"
TEST_USER_PASSWORD = "13579TfCWR"

@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = TEST_USER_PASSWORD
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')


@register
class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = "MyOwnBoard"


@register
class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    role = 1
    user = factory.SubFactory(UserFactory)


@register
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('title',)

    title = 'Category_one'
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)


@register
class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal


    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory, user=user)
    title = 'Some Title'
    description = 'some description'
    status = 1
    priority = 1
    due_date = '2022-02-22'
