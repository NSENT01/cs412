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
    path('post/<int:pk>', views.PostDetailView.as_view(), name="show_post"),
    path('profile/<int:pk>/create_post', views.CreatePostView.as_view(), name="create_post_form"),
    path('profile/<int:pk>/update', views.UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', views.DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', views.UpdatePostView.as_view(), name="update_post")
]