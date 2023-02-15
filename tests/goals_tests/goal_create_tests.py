import datetime

import pytest
from django.urls import reverse

from goals.models import Goal
from goals.serializers import GoalCreateSerializer
from tests.factories import BoardParticipantFactory, CategoryFactory

# ROUTE = '/goals/goal/create'

@pytest.mark.django_db
class TestGoalCreate:
    ROUTE_NAME = 'create goal'
    ROUTE_URL = reverse(ROUTE_NAME)

    def test_create_goal_by_user(self, client, test_user):
        client.force_login(test_user)

        goals_count_before = Goal.objects.count()

        category = CategoryFactory(user=test_user, title='my_category')
        BoardParticipantFactory(user=test_user, board=category.board, role=1)

        goal_data = {
            'category': category.id,
            'title': 'some_title',
            'description': 'some_description',
            'status': 1,
            'priority': 1,
            'due_date': str(datetime.date.today())
        }

        response = client.post(self.ROUTE_URL, data=goal_data)
        response_data = response.json()

        goals_count_after = Goal.objects.count()


        goal = Goal.objects.get(title=goal_data['title'], user=test_user)

        expected_response = GoalCreateSerializer(goal).data

        assert response.status_code == 201
        assert response_data == expected_response
        assert goals_count_after == goals_count_before+1

        for key, value in goal_data.items():
            assert value == response_data[key]

    def test_create_goal_by_anonymous(self, client, test_user):
        category = CategoryFactory(user=test_user, title='my_category')
        BoardParticipantFactory(user=test_user, board=category.board, role=1)

        goal_data = {
            'category': category.id,
            'title': 'some_title',
            'description': 'some_description',
            'status': 1,
            'priority': 1,
            'due_date': str(datetime.date.today())
        }

        expected_response = {
            'detail': 'Authentication credentials were not provided.'
        }

        response = client.post(self.ROUTE_URL, data=goal_data)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data == expected_response