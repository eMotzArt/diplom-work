import pytest
from django.urls import reverse

from core.models import User
from core.serializers import ProfileRetrieveUpdateSerializer

ROUTE = '/core/signup'

@pytest.mark.django_db
class TestSignup:
    ROUTE_NAME = 'signup view'
    ROUTE_URL = reverse(ROUTE_NAME)
    
    def test_signup_correct_data(self, client):
        post_data = {
            'username': 'testusername',
            'password': 'testpassword',
            'password_repeat': 'testpassword',
            'first_name': 'testfirstname',
            'last_name': 'testlastname',
            'email': 'testemail@test.ru',
        }
    
        response = client.post(self.ROUTE_URL, post_data)
    
        user = User.objects.get(username=post_data['username'])
    
        expected_response = {
            **ProfileRetrieveUpdateSerializer(user).data
        }
    
        assert response.status_code == 201
        assert response.json() == expected_response
    
    def test_signup_incorrect_repeat_password(self, client):
        post_data = {
            'username': 'testusername',
            'password': 'testpassword',
            'password_repeat': 'testpassword2',
            'first_name': 'testfirstname',
            'last_name': 'testlastname',
            'email': 'testemail@test.ru',
        }
    
        expected_response = {
            'non_field_errors': ['Passwords do not match']
        }
    
        response = client.post(self.ROUTE_URL, post_data)
    
    
    
        assert response.status_code == 400
        assert response.json() == expected_response