from django.urls import path
from core import views

urlpatterns = [
    path('signup', views.CreateUserView.as_view(), name='signup view'),
    path('login', views.LoginViaGenericAPIView.as_view(), name='login view'),
]
