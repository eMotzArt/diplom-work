import datetime

import pytest
from django.urls import reverse

from goals.serializers import GoalListSerializer
from tests.factories import GoalFactory, BoardParticipantFactory

# ROUTE = '/goals/goal/list'

@pytest.mark.django_db
class TestGoalsList:
    ROUTE_NAME = 'list goals'
    ROUTE_URL = reverse(ROUTE_NAME)
    
    def test_get_goal_list_by_user(self, client, test_user):
        goals_count = 15
    
        client.force_login(test_user)
    
        goals = GoalFactory.create_batch(goals_count, user=test_user)
        board = goals[0].category.board
        BoardParticipantFactory(user=test_user, board=board, role=1)
    
        expected_response = GoalListSerializer(goals, many=True).data
    
        response = client.get(self.ROUTE_URL)
        #
        assert response.status_code == 200
        assert response.json() == expected_response

    def test_get_goal_list_by_anonymous(self, client, test_user):
        goals_count = 15
    
        goals = GoalFactory.create_batch(goals_count, user=test_user)
        board = goals[0].category.board
        BoardParticipantFactory(user=test_user, board=board, role=1)
    
        expected_response = {
            'detail': 'Authentication credentials were not provided.',
        }
    
        response = client.get(self.ROUTE_URL)

        assert response.status_code == 403
        assert response.json() == expected_response
    
    def test_get_goal_list_by_user_with_pagination_page_1(self, client, test_user):
        goals_count = 15
        limit = 10
    
        client.force_login(test_user)
    
        goals = GoalFactory.create_batch(goals_count, user=test_user)
        board = goals[0].category.board
        BoardParticipantFactory(user=test_user, board=board, role=1)
    
        expected_response = {
            'count': goals_count,
            'next': f'http://testserver{self.ROUTE_URL}?limit={limit}&offset={limit}',
            'previous': None,
            'results': GoalListSerializer(goals, many=True).data[:limit],
        }
    
        response = client.get(self.ROUTE_URL, data={'limit': limit})

        assert response.status_code == 200
        assert response.json() == expected_response
    
    def test_get_goal_list_by_user_with_pagination_page_2(self, client, test_user):
        goals_count = 15
        limit = 10
    
        client.force_login(test_user)
    
        goals = GoalFactory.create_batch(goals_count, user=test_user)
        board = goals[0].category.board
        BoardParticipantFactory(user=test_user, board=board, role=1)
    
        expected_response = {
            'count': goals_count,
            'next': None,
            'previous': f'http://testserver{self.ROUTE_URL}?limit={limit}',
            'results': GoalListSerializer(goals, many=True).data[limit:],
        }
    
        response = client.get(self.ROUTE_URL, data={'limit': limit, 'offset': limit})

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_get_goal_list_by_user_with_ordering_by_priority(self, client, test_user):
        ordering_field = 'priority'

        client.force_login(test_user)
        goal_one = GoalFactory(user=test_user, priority=2)
        goal_two = GoalFactory(user=test_user, priority=3)
        goal_three = GoalFactory(user=test_user, priority=1)

        board = goal_one.category.board
        BoardParticipantFactory(user=test_user, board=board, role=1)

        expected_response = GoalListSerializer((goal_three, goal_one, goal_two), many=True).data

        response = client.get(self.ROUTE_URL, {'ordering': ordering_field})

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_get_goal_list_by_user_with_ordering_by_due_date(self, client, test_user):
        ordering_field = 'due_date'

        client.force_login(test_user)
        goal_one = GoalFactory(user=test_user, due_date=datetime.date.today()) #2nd
        goal_two = GoalFactory(user=test_user, due_date=datetime.date.today()-datetime.timedelta(days=4)) #1st
        goal_three = GoalFactory(user=test_user, due_date=datetime.date.today()+datetime.timedelta(days=2)) #3rd

        board = goal_one.category.board
        BoardParticipantFactory(user=test_user, board=board, role=1)

        expected_response = GoalListSerializer((goal_two, goal_one, goal_three), many=True).data

        response = client.get(self.ROUTE_URL, {'ordering': ordering_field})

        assert response.status_code == 200
        assert response.json() == expected_response