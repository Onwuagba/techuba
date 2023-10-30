from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.BasicView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('seeall/', views.ViewAllUsers.as_view()),
]
