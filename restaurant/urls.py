# File: restuarant/urls.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/20/2026
# Description: Defining the routes for the restaurant web page

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'main', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),
    
]