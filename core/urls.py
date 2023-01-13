from django.urls import path
from core import views

urlpatterns = [
    path('signup', views.CreateUserView.as_view(), name='signup view'),
    path('login', views.LoginViaGenericAPIView.as_view(), name='login view'),
    path('profile', views.ProfileView.as_view(), name='profile view'),
    path('update_password', views.PasswordUpdateView.as_view(), name='password update view'),
]
