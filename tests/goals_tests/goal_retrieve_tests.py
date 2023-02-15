import pytest
from django.urls import reverse

from goals.models import Goal
from goals.serializers import GoalListSerializer

# ROUTE = '/goals/goal/<pk:int>/'

@pytest.mark.django_db
class TestGoalRetrieve:
    ROUTE_NAME = 'retrieve goal'

    def test_retrieve_goal_by_user(self, client, test_user_with_goal):
        client.force_login(test_user_with_goal)
        goal = test_user_with_goal.goal_set.first()

        expected_response = GoalListSerializer(goal).data

        ROUTE_URL = reverse(self.ROUTE_NAME, kwargs={'pk': goal.id})
        response = client.get(ROUTE_URL)

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_retrieve_goal_by_anonymous(self, client, test_user_with_goal):
        goal = test_user_with_goal.goal_set.first()

        ROUTE_URL = reverse(self.ROUTE_NAME, kwargs={'pk': goal.id})
        expected_response = {
            'detail': 'Authentication credentials were not provided.'
        }

        response = client.get(ROUTE_URL)

        assert response.status_code == 403
        assert response.json() == expected_response

    def test_retrieve_not_existed_goal(self, client, test_user_with_goal):
        client.force_login(test_user_with_goal)

        goals_count = Goal.objects.count()


        expected_response = {
            'detail': 'Not found.'
        }

        ROUTE_URL = reverse(self.ROUTE_NAME, kwargs={'pk': goals_count+1})
        response = client.get(ROUTE_URL)

        assert response.status_code == 404
        assert response.json() == expected_response
