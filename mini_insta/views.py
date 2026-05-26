from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

# Create your views here.

class ProfileListView(ListView):
    '''Create a subclass of ListView to display all profiles'''

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''Create a subclass of DetailView to display one profile'''

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'
    

