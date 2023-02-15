import pytest
from django.urls import reverse

from core.models import User
from tests.fixtures import TEST_USER_NAME, TEST_USER_PASSWORD

ROUTE = '/core/update_password'


@pytest.mark.django_db
class TestUpdatePassword:
    ROUTE_NAME = 'password update view'
    ROUTE_URL = reverse(ROUTE_NAME)
        
    def test_update_password_by_user_correct_data(self, client, test_user):
        client.force_login(test_user)
    
        put_data = {
            'old_password': TEST_USER_PASSWORD,
            'new_password': 'new_test_password'
        }
    
        expected_response = {}
    
        response = client.put(self.ROUTE_URL, put_data)
    
        is_password_updated = User.objects.get(username=test_user.username).check_password(put_data['new_password'])
    
        assert response.status_code == 200
        assert response.json() == expected_response
        assert is_password_updated
    
    def test_update_password_by_user_incorrect_password(self, client, test_user):
        client.force_login(test_user)
    
        put_data = {
            'old_password': 'incorrect_password',
            'new_password': 'new_test_password'
        }
    
        expected_response = {
            'old_password': ['Password is incorrect'],
        }
    
        response = client.put(self.ROUTE_URL, put_data)
    
        assert response.status_code == 400
        assert response.json() == expected_response
    
    def test_update_password_by_user_easy_new_password(self, client, test_user):
        client.force_login(test_user)
    
        put_data = {
            'old_password': TEST_USER_PASSWORD,
            'new_password': '123'
        }
    
        expected_response = {
            'new_password': [
                'This password is too short. It must contain at least 8 characters.',
                'This password is too common.',
                'This password is entirely numeric.'
            ],
        }
    
        response = client.put(self.ROUTE_URL, put_data)
    
        assert response.status_code == 400
        assert response.json() == expected_response
    
    def test_update_password_by_anonymous(self, client, test_user):
        put_data = {
            'old_password': TEST_USER_PASSWORD,
            'new_password': '123'
        }
    
        expected_response = {
            'detail': 'Authentication credentials were not provided.'
        }
    
        response = client.put(self.ROUTE_URL, put_data)
    
        assert response.status_code == 403
        assert response.json() == expected_response
