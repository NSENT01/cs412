# File: mini_insta/models.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/22/2026
# Description: Defining the models used in our database

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of a social media profile'''

    username = models.CharField(max_length=50, unique=True)
    display_name = models.TextField(max_length=50, blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(max_length=100, blank=True)
    join_date = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''Return the string representation of the Profile model'''
        return f'{self.username}'

    def get_all_posts(self):
        '''Get all the posts for a profile and return as a QuerySet'''
        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_absolute_url(self):
        '''Redirect user to profile after successful update'''
        return reverse('profile', kwargs={'pk': self.pk})
    
    def get_followers(self):
        '''Get all profiles and return as a list'''
        ret = []
        for follower in Follower.objects.filter(profile=self):
            ret.append(follower.follower_profile)

        return ret
    
    def get_num_followers(self):
        '''Return the number of followers for a profile'''
        return len(self.get_followers())
    
    def get_following(self):
        '''Return list of profiles followed by this profile'''
        ret = []
        for following in Follower.objects.filter(follower_profile=self):
            ret.append(following.profile)

        return ret
    
    def get_num_following(self):
        '''Return the number of profiles this profile follows'''
        return len(self.get_following())
    
    def get_post_feed(self):
        '''Return a list of posts to serve as a feed'''
    
        posts = Post.objects.exclude(profile=self)

        # get the following and type cast to set for O(1) access
        following = set(self.get_following())

        # loop through all profiles, if they are in following set then skip, otherwise exclude
        for profile in Profile.objects.all():
            if profile in following:
                continue
            posts = posts.exclude(profile=profile)
        posts.order_by('timestamp')
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
    
    def get_all_comments(self):
        '''Return a list of all comments on a post object'''
        ret = []
        comments = Comment.objects.filter(post=self)
        for comment in comments:
            ret.append(comment)
        return ret
    
    def get_likes(self):
        '''Return a list of likes on a post object'''
        ret = []
        likes = Like.objects.filter(post=self)
        for like in likes:
            ret.append(like)
        return ret
    
    def get_num_likes_minus_1(self):
        '''Return the number of likes minus 1'''
        return len(self.get_likes()) - 1
    
    
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
        
class Follower(models.Model):
    '''Encapsulate the idea of an edge between two nodes representing profiles'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return the string representation of a follower'''
        return f'{self.follower_profile} follows {self.profile}'
    
class Comment(models.Model):
    '''Encapsulate the idea of a comment on a post'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        '''Return the string representation of a comment'''
        return f'{self.profile} commented {self.text} on {self.post}'

class Like(models.Model):
    '''Encapsulate the idea of a like on a post'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of a like'''
        return f'{self.profile} liked {self.post}'