import pytest
from django.urls import reverse

from goals.serializers import GoalListSerializer
from tests.factories import BoardParticipantFactory


# ROUTE = '/goals/goal/<pk:int>/'

@pytest.mark.django_db
class TestGoalRetrieveByParticipant:
    ROUTE_NAME = 'retrieve goal'

    def test_retrieve_goal_by_participant(self, client, test_user_with_goal, test_second_user):
        client.force_login(test_second_user)

        goal = test_user_with_goal.goal_set.first()

        BoardParticipantFactory(board=goal.category.board, user=test_second_user, role=3)

        expected_response = GoalListSerializer(goal).data

        ROUTE_URL = reverse(self.ROUTE_NAME, kwargs={'pk': goal.id})
        response = client.get(ROUTE_URL)

        assert response.status_code == 200
        assert response.json() == expected_response

