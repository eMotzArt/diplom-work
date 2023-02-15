import datetime

import pytest
from django.urls import reverse

from tests.factories import BoardParticipantFactory, CategoryFactory

# ROUTE = '/goals/goal/create'

@pytest.mark.django_db
class TestGoalCreateByParticipant:
    ROUTE_NAME = 'create goal'
    ROUTE_URL = reverse(ROUTE_NAME)

    def test_create_goal_by_participant(self, client, test_user, test_second_user):
        client.force_login(test_second_user)

        category = CategoryFactory(user=test_user, title='my_category')
        BoardParticipantFactory(user=test_second_user, board=category.board, role=3)

        goal_data = {
            'category': category.id,
            'title': 'some_title',
            'description': 'some_description',
            'status': 1,
            'priority': 1,
            'due_date': str(datetime.date.today())
        }

        expected_response = {
            'detail': 'You do not have permission to perform this action.'
        }

        response = client.post(self.ROUTE_URL, data=goal_data)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data == expected_response
