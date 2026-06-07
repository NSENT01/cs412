# File: mini_insta/urls.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/22/2026
# Description: Defining the routes for the mini insta web app

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

# url patterns for mini insta
urlpatterns = [
    path('', views.ProfileListView.as_view(), name="home"),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name="profile"),
    path('post/<int:pk>', views.PostDetailView.as_view(), name="show_post"),
    path('profile/create_post', views.CreatePostView.as_view(), name="create_post_form"),
    path('profile/update', views.UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', views.DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', views.UpdatePostView.as_view(), name="update_post"),
    path('profile/<int:pk>/following', views.ShowFollowingDetailView.as_view(), name="show_following"),
    path('profile/<int:pk>/followers', views.ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/feed', views.ShowFeedView.as_view(), name="show_feed"),
    path('profile/search', views.SearchView.as_view(), name="search"),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path('profile/', views.PersonalProfileDetailView.as_view(), name="personal_profile"),
    path('register/', views.CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/follow', views.CreateFollowView.as_view(), name="follow"),
    path('profile/<int:pk>/delete_follow', views.DeleteFollowView.as_view(), name="delete_follow"),
    path('post/<int:pk>/like', views.CreateLikeView.as_view(), name="like"),
    path('post/<int:pk>/delete_like', views.DeleteLikeView.as_view(), name="delete_like"),
]