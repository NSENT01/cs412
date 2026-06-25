# File: spiy/urls.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 6/12/2026
# Description: Defining the routes for the sipy web app

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profiles/', views.ProfileListView.as_view(), name="profile_list"),
    path('cafes/', views.CafeListView.as_view(), name="cafe_list"),
    path('drinks/', views.DrinkListView.as_view(), name="drink_list"),
    path('rankings/', views.RankingListView.as_view(), name="ranking_list"),
    path('want-to-try/', views.WantToTryListView.as_view(), name="want_to_try_list"),
    path('follows/', views.FollowListView.as_view(), name="follow_list"),
    path('likes/', views.LikeListView.as_view(), name="like_list"),
    path('comments/', views.CommentListView.as_view(), name="comment_list"),
    path('api/register/', views.CreateAccountView.as_view(), name="register"),
    path('api/get_profile/', views.GetSingleProfileView.as_view(), name="get_profile"),
    path('api/update_profile/', views.UpdateProfileView.as_view(), name="update_profile"),
    path('api/delete_profile/', views.DeleteProfileView.as_view(), name="delete_profile"),
    path('api/get_other_profile/', views.GetOtherProfileView.as_view(), name="get_other_profile"),
    path('api/get_profiles/', views.GetAllProfilesView.as_view(), name="get_profiles"),
    path('api/get_cafe/', views.GetCafeView.as_view(), name="get_cafe"),
    path('api/create_cafe/', views.CreateCafeView.as_view(), name="create_cafe"),
    path('api/get_ranking/', views.GetRankingView.as_view(), name="get_ranking"),
    path('api/create_ranking/', views.CreateRankingView.as_view(), name="create_ranking"),
    path('api/delete_ranking/', views.DestroyRankingView.as_view(), name="delete_ranking"),
    path('api/create_follow/', views.CreateFollowView.as_view(), name="create_follow"),
    path('api/get_follow/', views.GetFollowView.as_view(), name="get_follow"),
    path('api/get_following/', views.GetFollowingView.as_view(), name="get_following"),
    path('api/get_followers/', views.GetFollowersView.as_view(), name="get_followers"),
    path('api/delete_follow/', views.DestroyFollowView.as_view(), name="destroy_view"),
    path('api/get_taste_profile/', views.GetTasteProfileView.as_view(), name="get_taste_profile"),
    path('api/create_wanttotry/', views.CreateWantToTryView.as_view(), name="create_wanttotry"),
    path('api/get_wanttotry/', views.GetWantToTryView.as_view(), name="get_wanttotry"),
    path('api/delete_wanttotry/', views.DeleteWantToTryView.as_view(), name="delete_wanttotry"),
    path('api/search_profiles/', views.ProfileSearchView.as_view(), name='search_profiles'),
    path('api/create_like/', views.CreateLikeView.as_view(), name="create_like"),
    path('api/delete_like/', views.DeleteLikeView.as_view(), name="delete_like"),
    path('api/create_comment/', views.CreateCommentView.as_view(), name="create_comment"),
    path('api/delete_comment/', views.DeleteCommentView.as_view(), name="delete_comment"),
]
