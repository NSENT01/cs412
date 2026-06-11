# File: mini_insta/views.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/22/2026
# Description: API for rendering HTML form and handling input data

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class ProfileListView(ListView):
    '''Create a subclass of ListView to display all profiles'''

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = "profiles"

    def get_context_data(self, **kwargs):
        '''Override this method to add context variable profile'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            context['profile'] = profile

        return context

class ProfileDetailView(DetailView):
    '''Create a subclass of DetailView to display one profile'''

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'other_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            context['profile'] = profile

            follows = Follower.objects.filter(follower_profile=profile).values_list('profile', flat=True)

            context['follows'] = follows

        return context

class PersonalProfileDetailView(LoginRequiredMixin, DetailView):
    '''Create a subclass of DetailView to display the profile of the logged in user'''

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'other_profile'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_context_data(self, **kwargs):
        '''Add context variables'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile

        return context

    def get_object(self, queryset = ...):
        '''Define the context object based on the logged in user'''
        return Profile.objects.get(user=self.request.user)
    
class CreatePostView(LoginRequiredMixin, CreateView):
    '''Create a subclass of CreateView to handle the creation of a new post'''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_context_data(self):
        '''Give context data for url routing'''
        context = super().get_context_data()

        # get the Profile object with the primary key in the route and append it to the context
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Post
        object before saving it to the database.
        '''
        self.profile = Profile.objects.get(user=self.request.user)
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
        return reverse('personal_profile')


class PostDetailView(DetailView):
    '''Create a subclass of DetailView to display one post'''

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''Override this method to add profile context variable'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            context['profile'] = profile
            context['likes'] = Like.objects.filter(profile=profile).values_list('post_id', flat=True)

        return context

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''Create a subclass of UpdateView to update a posts data in our database'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_object(self):
        '''Define the context object based on the logged in user'''
        if self.request.user.is_authenticated:
            return Profile.objects.get(user=self.request.user)
        else:
            return Profile.objects.none()

class DeletePostView(LoginRequiredMixin, DeleteView):
    '''Create a subclass of DeleteView to delete a post from our database'''

    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        '''Give context data for url routing'''
        context = super().get_context_data(**kwargs)

        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])

        context['profile'] = Profile.objects.get(user=self.request.user)
        return context
    
    def get_queryset(self):
        '''Define a queryset for which this view can delete posts'''
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            return Post.objects.filter(profile=profile)
        else:
            return Post.objects.none()
    
    def get_success_url(self):
        '''Define the URL to which succesful deletion should redirect the user'''

        return reverse('personal_profile')
    
class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''Create a subclass of UpdateView to update a post in our database'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_context_data(self, **kwargs):
        '''Override this method to add post and profile context variables'''
        context =  super().get_context_data(**kwargs)

        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])

        context['profile'] = Profile.objects.get(user=self.request.user)
        return context
    
    def get_queryset(self):
        '''Define the queryset for which this view can update posts'''
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            return Post.objects.filter(profile=profile)
        else:
            return Post.objects.none()
    
    def get_success_url(self):
        '''Define a redirection url after this view executes succesfully'''
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


class ShowFeedView(LoginRequiredMixin, DetailView):
    '''Create a subclass of DetailView to show a users feed'''

    model = Profile
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'profile'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        likes = Like.objects.filter(profile=profile).values_list('post_id', flat=True)
        context['likes'] = likes

        return context

    def get_object(self, queryset = ...):
        return Profile.objects.get(user=self.request.user)

class SearchView(LoginRequiredMixin, ListView):
    '''Create a subclass of ListView to show search results'''


    template_name = 'mini_insta/search_results.html'
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        '''Override dispatch method to return based on incoming form data'''
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        
        # get general context objects to facilitate search
        profile = Profile.objects.get(user=self.request.user)
        likes = Like.objects.filter(profile=profile).values_list('post_id', flat=True)
        context = {
            'profile': profile,
            'likes': likes,
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
        
        profile = Profile.objects.get(user=self.request.user)
        name = self.request.GET['name']
        posts = Post.objects.filter(profile__username__icontains=name) | Post.objects.filter(profile__display_name__icontains=name) | Post.objects.filter(caption__icontains=name)
        posts = posts.exclude(profile=profile)

        return posts
    
    def get_context_data(self, **kwargs):
        '''Override this method to add profile, profiles, and posts context'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        context['posts'] = self.get_queryset()

        # get context objects for search request
        if 'name' in self.request.GET:
            name = self.request.GET['name']
            context['profiles'] = Profile.objects.filter(username__icontains=name) | Profile.objects.filter(display_name__icontains=name)
            context['profiles'] = context['profiles'].exclude(username=profile.username).exclude(display_name=profile.display_name)
        else:
            context['profiles'] = Profile.objects.none()

        return context
    
class CreateProfileView(CreateView):
    '''Create a subclass of CreateView to create a profile and user in our db'''

    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        '''Override this method to add the appropriate context variables'''
        context =  super().get_context_data(**kwargs)

        context['create_user'] = UserCreationForm()

        return context
    
    def form_valid(self, form):
        '''Define how the form should write to the database'''
        if self.request.POST:
            create_user = UserCreationForm(self.request.POST)

        
        user = create_user.save()
        # automatically log in when account is created
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        form.instance.user = user

        return super().form_valid(form)
    
    def get_success_url(self):
        '''Define the redirect url when this view executes succesfully'''
        return reverse('personal_profile')

class CreateFollowView(TemplateView):
    '''Create subclass of TemplateView to create a follow instance'''


    def dispatch(self, request, *args, **kwargs):
        '''Override the default method to create follow instance'''
        follower_profile = Profile.objects.get(user=request.user)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # create follow based on retrieved profile
        Follower.objects.create(profile=profile, follower_profile=follower_profile)
        return redirect('profile', pk=profile.pk)
    
class DeleteFollowView(TemplateView):
    '''Create subclass of TemplateView to delete a follow instance'''

    def dispatch(self, request, *args, **kwargs):
        '''Override the default method to delete follow instance'''
        follower_profile = Profile.objects.get(user=request.user)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # delete follow based on retrieved profile
        Follower.objects.filter(follower_profile=follower_profile).filter(profile=profile).delete()
        return redirect('profile', pk=profile.pk)

class CreateLikeView(TemplateView):
    '''Create a subclass of TemplateView to create a like instance'''

    def dispatch(self, request, *args, **kwargs):
        '''Override the default method to create like instance'''
        if 'pk' in self.kwargs:
            # get post
            post = Post.objects.get(pk=self.kwargs['pk'])
        profile = Profile.objects.get(user=request.user)
        # create like on post
        Like.objects.create(post=post, profile=profile)
        return redirect('show_post', pk=post.pk)
    
class DeleteLikeView(TemplateView):
    '''Create a subclass of TemplateView to delete a like instance'''

    def dispatch(self, request, *args, **kwargs):
        '''Override the default method to delete like instance'''
        if 'pk' in self.kwargs:
            # get post
            post = Post.objects.get(pk=self.kwargs['pk'])
        profile = Profile.objects.get(user=request.user)
        # delete like on post
        Like.objects.filter(post=post).filter(profile=profile).delete()
        return redirect('show_post', pk=post.pk)

