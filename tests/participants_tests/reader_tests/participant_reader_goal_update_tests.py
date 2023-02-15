import pytest
from django.urls import reverse

from core.serializers import ProfileRetrieveUpdateSerializer
from goals.models import Goal
from tests.factories import CategoryFactory, BoardParticipantFactory


@pytest.mark.django_db
class TestGoalUpdate:
    ROUTE_NAME = 'retrieve goal'

    def test_update_goal_by_user(self, client, test_user_with_goal, test_second_user):
        client.force_login(test_second_user)
        goal = test_user_with_goal.goal_set.first()
        new_category = CategoryFactory(title='new_cat', board=goal.category.board, user=test_user_with_goal)
        BoardParticipantFactory(board=goal.category.board, user=test_second_user, role=3)

        new_goal_data = {
            "title": "updated_title",
            "description": "updated_description",
            "due_date": "2023-01-01",
            "status": 2,
            "priority": 2,
            "category": new_category.id
        }

        expected_response = {
            'detail': 'You do not have permission to perform this action.'
        }

        ROUTE_URL = reverse(self.ROUTE_NAME, kwargs={'pk': goal.id})
        response = client.put(ROUTE_URL, data=new_goal_data)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data == expected_response
