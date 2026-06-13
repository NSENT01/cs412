# File: spiy/urls.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 6/12/2026
# Description: Defining the routes for the mini insta web app

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/register/', views.CreateAccountView.as_view(), name="register"),
]