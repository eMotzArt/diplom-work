from django.urls import path
from bot import views


urlpatterns = [
    #goal_category
    path('verify', views.BotVerification.as_view()),

]
