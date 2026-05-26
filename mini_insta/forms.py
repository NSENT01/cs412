# File: mini_insta/forms.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/26/2026
# Description: Defining how form data will be written to our databse using our specified model classes

from django import forms
from .models import Post

class CreatePost(forms.ModelForm):
    '''Writes a new Post to our database'''

    class Meta:
        '''Associate this form with a model from out database'''
        model = Post
        fields = ['']
