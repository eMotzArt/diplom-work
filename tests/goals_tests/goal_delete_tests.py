import pytest
from django.urls import reverse

from goals.models import Goal
from goals.serializers import GoalListSerializer

# ROUTE = '/goals/goal/<pk:int>/'

@pytest.mark.django_db
class TestGoalRetrieve:
    ROUTE_NAME = 'retrieve goal'

    def test_delete_goal_by_user(self, client, test_user_with_goal):
        client.force_login(test_user_with_goal)
        goal = test_user_with_goal.goal_set.first()

        ROUTE_URL = reverse(self.ROUTE_NAME, kwargs={'pk': goal.id})
        response = client.delete(ROUTE_URL)

        deleted_goal = test_user_with_goal.goal_set.get(id=goal.id)
        assert deleted_goal.status == 4
        assert response.status_code == 204

    def test_delete_goal_by_anonymous(self, client, test_user_with_goal):
        goal = test_user_with_goal.goal_set.first()

        ROUTE_URL = reverse(self.ROUTE_NAME, kwargs={'pk': goal.id})
        expected_response = {
            'detail': 'Authentication credentials were not provided.'
        }

        response = client.get(ROUTE_URL)

        assert response.status_code == 403
        assert response.json() == expected_response
