# File: dadjokes/urls.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 06/10/2026
# Description: Defining the routes for the dadjokes web app

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.randomJoke, name="home"),
    path('random/', views.randomJoke, name="random"),
    path('pictures/', views.PictureListView.as_view(), name="pictures"),
    path('picture/<int:pk>/', views.PictureDetailView.as_view(), name="picture"),
    path('jokes/', views.JokeListView.as_view(), name="jokes"),
    path('joke/<int:pk>/', views.JokeDetailView.as_view(), name="joke")
]