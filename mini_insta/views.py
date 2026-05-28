# File: mini_insta/views.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/22/2026
# Description: API for rendering HTML form and handling input data

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import CreatePostForm
from django.shortcuts import get_object_or_404
from django.urls import reverse

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
    
class CreatePostView(CreateView):
    '''Create a subclass of CreateView to handle the creation of a new post'''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self):
        '''Give context data for url routing'''
        context = super().get_context_data()
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Post
        object before saving it to the database.
        '''
        self.profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = self.profile

        # allow the post to be created so it can be used to create a photo object associated with it
        response = super().form_valid(form)

        # if self.request.POST:
        #     image_url = self.request.POST['image_url']
        #     Photo.objects.create(
        #         image_url = image_url,
        #         post = self.object
        #     )

        files = self.request.FILES.getlist('image_files')
        for file in files:
            Photo.objects.create(
                image_file = file,
                post = self.object
            )

        return response


class PostDetailView(DetailView):
    '''Create a subclass of DetailView to display one post'''

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'



