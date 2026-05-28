# File: mini_insta/models.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/22/2026
# Description: Defining the models used in our database

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of a social media profile'''

    username = models.CharField(max_length=50, unique=True)
    display_name = models.TextField(max_length=50, blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(max_length=100, blank=True)
    join_date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        '''Return the string representation of the Profile model'''
        return f'{self.username}'

    def get_all_posts(self):
        '''Get all the posts for a profile and return as a QuerySet'''
        posts = Post.objects.filter(profile=self)
        return posts

    
class Post(models.Model):
    '''Encapsulate the idea of a social media post'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''Return the string representation of the Post model'''
        return f'{self.profile}:{self.pk}'
    
    def get_all_photos(self):
        '''Get all the posts for a post and return as a QuerySet'''
        photos = Photo.objects.filter(post=self)
        return photos
    
    def get_absolute_url(self):
        '''Return success url after post has been created'''
        return reverse('show_post', kwargs={'pk': self.pk})
    
class Photo(models.Model):
    '''Encapsulate the idea of a posts photo'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        '''Return the string representation of the Photo model'''
        return f'{self.post}:{self.pk}'
    
    def get_image_url(self):
        '''Return the image url, handling if its a link or a file'''
        if self.image_url:
            return self.image_url
        else:
            return self.image_file.url
    