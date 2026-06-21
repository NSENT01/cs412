# File: spiy/urls.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 6/12/2026
# Description: Defining the routes for the mini insta web app

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/register/', views.CreateAccountView.as_view(), name="register"),
    path('api/get_profile/', views.GetSingleProfileView.as_view(), name="get_profile"),
    path('api/get_other_profile/', views.GetOtherProfileView.as_view(), name="get_other_profile"),
    path('api/get_profiles/', views.GetAllProfilesView.as_view(), name="get_profiles"),
    path('api/get_cafe/', views.GetCafeView.as_view(), name="get_cafe"),
    path('api/create_cafe/', views.CreateCafeView.as_view(), name="create_cafe"),
    path('api/get_drink/', views.GetDrinkView.as_view(), name="get_drink"),
    path('api/create_drink/', views.CreateDrinkView.as_view(), name="create_drink"),
    path('api/get_ranking/', views.GetRankingView.as_view(), name="get_ranking"),
    path('api/create_ranking/', views.CreateRankingView.as_view(), name="create_ranking"),
    path('api/delete_ranking/', views.DestroyRankingView.as_view(), name="delete_ranking"),
    path('api/create_follow/', views.CreateFollowView.as_view(), name="create_follow"),
    path('api/delete_follow/', views.DestroyFollowView.as_view(), name="destroy_view"),
]