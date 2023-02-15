import pytest

from tests.factories import BoardFactory, CategoryFactory, GoalFactory, BoardParticipantFactory

TEST_USER_NAME = 'testuser1'
TEST_USER_PASSWORD = '13579TfCWR'
TEST_USER_EMAIL = 'test@test.ru'

@pytest.fixture()
def client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def test_user(django_user_model):
    user_data = {
        "username": TEST_USER_NAME,
        "first_name": "test user first name",
        "last_name": "test user last name",
        "password": TEST_USER_PASSWORD,
        "email": TEST_USER_EMAIL,
    }
    user = django_user_model.objects.create(**user_data)
    user.set_password(user.password)
    user.save()

    return user

@pytest.fixture
@pytest.mark.django_db
def test_user_with_goal(django_user_model, test_user):
    board = BoardFactory()
    category = CategoryFactory(board=board, user=test_user)
    goal = GoalFactory(user=test_user, category=category)
    board_participant = BoardParticipantFactory(board=board, user=test_user, role=1)
    return test_user

@pytest.fixture
@pytest.mark.django_db
def test_user_board(django_user_model, test_user_with_goal):
    board = test_user_with_goal.goal_set.first().category.board
    return board

@pytest.fixture
@pytest.mark.django_db
def test_second_user(django_user_model):
    user_data = {
        "username": 'second_user',
        "first_name": "test user first name",
        "last_name": "test user last name",
        "password": TEST_USER_PASSWORD,
        "email": 'second@test.ru',
    }
    user = django_user_model.objects.create(**user_data)
    user.set_password(user.password)
    user.save()

    return user

@pytest.fixture
@pytest.mark.django_db
def test_second_user_with_goal(django_user_model, test_second_user):
    board = BoardFactory()
    category = CategoryFactory(board=board, user=test_second_user)
    goal = GoalFactory(user=test_second_user, category=category)
    board_participant = BoardParticipantFactory(board=board, user=test_second_user, role=1)
    return test_second_user

