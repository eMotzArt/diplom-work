import pytest
from django.urls import reverse

from core.serializers import ProfileRetrieveUpdateSerializer

# ROUTE = '/core/profile'

@pytest.mark.django_db
class TestProfile:
    ROUTE_NAME = 'profile view'
    ROUTE_URL = reverse(ROUTE_NAME)

    def test_get_profile_by_anonymous(self, client, test_user):
        expected_response = {
            'detail': 'Authentication credentials were not provided.'
        }
    
        response = client.get(self.ROUTE_URL)
    
        assert response.status_code == 403
        assert response.json() == expected_response
    
    def test_get_profile_by_user(self, client, test_user):
        client.force_login(test_user)
        expected_response = {
            **ProfileRetrieveUpdateSerializer(test_user).data
        }
    
        response = client.get(self.ROUTE_URL)
    
        assert response.status_code == 200
        assert response.json() == expected_response