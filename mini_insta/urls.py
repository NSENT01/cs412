# File: mini_insta/urls.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/22/2026
# Description: Defining the routes for the mini insta web app

from django.urls import path
from django.conf import settings
from . import views

# url patterns for mini insta
urlpatterns = [
    path('', views.ProfileListView.as_view(), name="home"),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name="profile"),
]