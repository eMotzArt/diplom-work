import pytest
from django.urls import reverse

from core.serializers import ProfileRetrieveUpdateSerializer
from goals.models import Goal
from tests.factories import CategoryFactory


@pytest.mark.django_db
class TestGoalUpdate:
    ROUTE_NAME = 'retrieve goal'

    def test_update_goal_by_user(self, client, test_user_with_goal):
        client.force_login(test_user_with_goal)
        goal = test_user_with_goal.goal_set.first()
        new_category = CategoryFactory(title='new_cat', board=goal.category.board, user=test_user_with_goal)
        new_goal_data = {
            "title": "updated_title",
            "description": "updated_description",
            "due_date": "2023-01-01",
            "status": 2,
            "priority": 2,
            "category": new_category.id
        }

        expected_response = {
            'id': goal.id,
            'user': ProfileRetrieveUpdateSerializer(test_user_with_goal).data,
            **new_goal_data
        }

        ROUTE_URL = reverse(self.ROUTE_NAME, kwargs={'pk': goal.id})
        response = client.put(ROUTE_URL, data=new_goal_data)
        response_data = response.json()

        assert response.status_code == 200
        for key, value in expected_response.items():
            assert response_data.get(key) == value

    def test_update_goal_by_anonymous(self, client, test_user_with_goal):
        goal = test_user_with_goal.goal_set.first()
        new_category = CategoryFactory(title='new_cat', board=goal.category.board, user=test_user_with_goal)
        new_goal_data = {
            "title": "updated_title",
            "description": "updated_description",
            "due_date": "2023-01-01",
            "status": 2,
            "priority": 2,
            "category": new_category.id
        }

        expected_response = {
            'detail': 'Authentication credentials were not provided.'
        }

        ROUTE_URL = reverse(self.ROUTE_NAME, kwargs={'pk': goal.id})
        response = client.put(ROUTE_URL, data=new_goal_data)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data == expected_response

    def test_update_by_user_goal_not_existed(self, client, test_user_with_goal):
        client.force_login(test_user_with_goal)
        goals_count = Goal.objects.count()
        new_goal_data = {
            "title": "updated_title",
            "description": "updated_description",
            "due_date": "2023-01-01",
            "status": 2,
            "priority": 2,
            "category": 2
        }

        expected_response = {
            'detail': 'Not found.'
        }

        ROUTE_URL = reverse(self.ROUTE_NAME, kwargs={'pk': goals_count+1})
        response = client.put(ROUTE_URL, data=new_goal_data)
        response_data = response.json()

        assert response.status_code == 404
        assert response_data == expected_response