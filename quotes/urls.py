# File: urls.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/18/2026
# Description: Defining the routes for the quotes web page

from django.urls import path
from django.conf import settings
from . import views

# url patters for quotes app
urlpatterns = [
    path(r'', views.home, name="home"),
    path(r'quote', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"),
    path(r'about', views.about, name="about")
]