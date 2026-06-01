# File: mini_insta/forms.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/26/2026
# Description: Defining how form data will be written to our databse using our specified model classes

from django import forms
from .models import Post, Profile

class CreatePostForm(forms.ModelForm):
    '''Writes a new Post to our database'''

    class Meta:
        '''Associate this form with a model from out database'''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''Updates a Post record to our database'''

    class Meta:
        '''Associate this form with the appropriate model'''
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url']
