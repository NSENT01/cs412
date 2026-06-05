# File: mini_insta/views.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/22/2026
# Description: API for rendering HTML form and handling input data

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
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

        # get the Profile object with the primary key in the route and append it to the context
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

        # iterate through all photos and make a new instance of the object with the appropriate post field
        files = self.request.FILES.getlist('image_files')
        for file in files:
            Photo.objects.create(
                image_file = file,
                post = self.object
            )

        return response
    
    def get_success_url(self):
        '''Get url for redirection after succesful creation of post'''
        return reverse('profile', kwargs={'pk': self.kwargs['pk']})


class PostDetailView(DetailView):
    '''Create a subclass of DetailView to display one post'''

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class UpdateProfileView(UpdateView):
    '''Create a subclass of UpdateView to update a posts data in our database'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class DeletePostView(DeleteView):
    '''Create a subclass of DeleteView to delete a post from our database'''

    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        '''Give context data for url routing'''
        context = super().get_context_data(**kwargs)

        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])

        context['profile'] = context['post'].profile
        return context
    
    def get_success_url(self):
        '''Define the URL to which succesful deletion should redirect the user'''

        profile_pk = get_object_or_404(Post, pk=self.kwargs['pk']).profile.pk

        return reverse('profile', kwargs={'pk': profile_pk})
    
class UpdatePostView(UpdateView):
    '''Create a subclass of UpdateView to update a post in our database'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])

        context['profile'] = context['post'].profile
        return context
    
    def get_success_url(self):
        return reverse('show_post', kwargs={'pk': self.kwargs['pk']})
    
class ShowFollowingDetailView(DetailView):
    '''Create a subclass of DetailView to show a users entire following'''
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class ShowFollowersDetailView(DetailView):
    '''Create a subclass of DetailView to show a users followers'''

    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFeedView(DetailView):
    '''Create a subclass of DetailView to show a users feed'''

    model = Profile
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'profile'

class SearchView(ListView):
    '''Create a subclass of ListView to show search results'''


    template_name = 'mini_insta/search_results.html'

    def dispatch(self, request, *args, **kwargs):
        '''Override dispatch method to return based on incoming form data'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context = {
            'profile': profile,
        }
        if 'name' in self.request.GET:
            return super().dispatch(request, *args, **kwargs)
        else:
            template = 'mini_insta/search.html'
            return render(request, template, context)
        
    def get_queryset(self):
        '''Return the queryset of Posts for the ListView since a model was not specified'''
        if 'name' not in self.request.GET:
            return Post.objects.none()
        
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        name = self.request.GET['name']
        posts = Post.objects.filter(profile__username__icontains=name) | Post.objects.filter(profile__display_name__icontains=name) | Post.objects.filter(caption__contains=name)
        posts = posts.exclude(profile=profile)

        return posts
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        context['posts'] = self.get_queryset()

        if 'name' in self.request.GET:
            name = self.request.GET['name']
            context['profiles'] = Profile.objects.filter(username__icontains=name) | Profile.objects.filter(display_name__icontains=name)
            context['profiles'] = context['profiles'].exclude(username=profile.username).exclude(display_name=profile.display_name)
        else:
            context['profiles'] = Profile.objects.none()

        return context
