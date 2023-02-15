import pytest
from django.urls import reverse

from core.serializers import ProfileRetrieveUpdateSerializer
from tests.fixtures import TEST_USER_NAME, TEST_USER_PASSWORD

# ROUTE = '/core/login'

@pytest.mark.django_db
class TestLogin:
    ROUTE_NAME = 'login view'
    ROUTE_URL = reverse(ROUTE_NAME)

    def test_login_correct_data(self, client, test_user):
        post_data = {
            'username': TEST_USER_NAME,
            'password': TEST_USER_PASSWORD
        }
    
        expected_response = {
            **ProfileRetrieveUpdateSerializer(test_user).data
        }
    
        response = client.post(self.ROUTE_URL, post_data)
    
        assert response.status_code == 200
        assert response.json() == expected_response
    
    def test_login_incorrect_password(self, client, test_user):
        post_data = {
            'username': TEST_USER_NAME,
            'password': 'wrong_password',
        }
    
        expected_response = {
            'non_field_errors': ['Username or password is incorrect']
        }
    
        response = client.post(self.ROUTE_URL, post_data)
    
        assert response.status_code == 400
        assert response.json() == expected_response
    
    def test_login_incorrect_username(self, client, test_user):
        post_data = {
            'username': 'wrong_name',
            'password': TEST_USER_PASSWORD
        }
    
        expected_response = {
            'non_field_errors': ['Username or password is incorrect']
        }
    
        response = client.post(self.ROUTE_URL, post_data)
    
        assert response.status_code == 400
        assert response.json() == expected_response
    
    def test_login_incorrect_password_and_username(self, client, test_user):
        post_data = {
            'username': 'wrong_name',
            'password': 'wrong_password'
        }
    
        expected_response = {
            'non_field_errors': ['Username or password is incorrect']
        }
    
        response = client.post(self.ROUTE_URL, post_data)
    
        assert response.status_code == 400
        assert response.json() == expected_response
