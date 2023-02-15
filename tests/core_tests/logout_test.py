import pytest
from django.urls import reverse

# ROUTE = '/core/profile'

@pytest.mark.django_db
class TestLogout:
    ROUTE_NAME = 'profile view'
    ROUTE_URL = reverse(ROUTE_NAME)

    def test_logout_anonymous(self, client, test_user):
        expected_response = {
            'detail': 'Authentication credentials were not provided.'
        }

        response = client.delete(self.ROUTE_URL)

        assert response.status_code == 403
        assert response.json() == expected_response

    def test_logout_by_user(self, client, test_user):
        client.force_login(test_user)
        assert client.session.session_key
    
        response = client.delete(self.ROUTE_URL)
    
        assert not client.session.session_key
        assert response.status_code == 204
    
    
