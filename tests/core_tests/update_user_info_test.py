import pytest
from django.urls import reverse

from tests.factories import UserFactory

# ROUTE = '/core/update_password'


@pytest.mark.django_db
class TestUpdateUserInfo:
    ROUTE_NAME = 'profile view'
    ROUTE_URL = reverse(ROUTE_NAME)

    def test_update_user_correct_data_by_user(self, client, test_user):
        client.force_login(test_user)

        put_data = {
            'username': 'new_user_name',
            'first_name': 'new_first_name',
            'last_name': 'new_last_name',
            'email': 'new_email@test.ru'
        }

        expected_response = {
            'id': test_user.id,
            **put_data
        }
    
        response = client.put(self.ROUTE_URL, put_data)
    
        assert response.status_code == 200
        assert response.json() == expected_response

    def test_update_user_correct_data_by_anonymous(self, client, test_user):
        put_data = {
            'username': 'new_user_name',
            'first_name': 'new_first_name',
            'last_name': 'new_last_name',
            'email': 'new_email@test.ru'
        }

        expected_response = {
            'detail': 'Authentication credentials were not provided.'
        }

        response = client.put(self.ROUTE_URL, put_data)

        assert response.status_code == 403
        assert response.json() == expected_response

    def test_update_user_data_by_user_username_already_exists(self, client, test_user):
        client.force_login(test_user)
        new_user = UserFactory(username='name_holder')
        put_data = {
            'username': new_user.username,
            'first_name': 'new_first_name',
            'last_name': 'new_last_name',
            'email': 'new_email@test.ru'
        }

        expected_response = {
            'username': ['A user with that username already exists.']
        }

        response = client.put(self.ROUTE_URL, put_data)

        assert response.status_code == 400
        assert response.json() == expected_response
