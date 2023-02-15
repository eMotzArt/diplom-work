import pytest
from django.urls import reverse

from tests.factories import BoardParticipantFactory


# ROUTE = '/goals/goal/<pk:int>/'

@pytest.mark.django_db
class TestGoalRetrieve:
    ROUTE_NAME = 'retrieve goal'

    def test_delete_goal_by_participant(self, client, test_user_with_goal, test_second_user):
        client.force_login(test_second_user)
        goal = test_user_with_goal.goal_set.first()
        BoardParticipantFactory(board=goal.category.board, user=test_second_user, role=3)

        expected_response = {
            'detail': 'You do not have permission to perform this action.'
        }

        ROUTE_URL = reverse(self.ROUTE_NAME, kwargs={'pk': goal.id})
        response = client.delete(ROUTE_URL)

        deleted_goal = test_user_with_goal.goal_set.get(id=goal.id)
        assert response.status_code == 403
        assert response.json() == expected_response
