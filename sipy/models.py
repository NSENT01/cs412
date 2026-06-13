from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of a user profile'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_user")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_image = models.ImageField(blank=True)
    bio_text = models.TextField(blank=True)

class Cafe(models.Model):
    '''Encapsulate the idea of a cafe item'''
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


class Drink(models.Model):
    '''Encapsulate the idea of a drink from a cafe'''

class Ranking(models.Model):
    '''Encapsulate the idea of a drink ranking'''

class WantToTry(models.Model):
    '''Encapsulate the idea of a want to try list'''

class Follow(models.Model):
    '''Encapsulate the idea of a follow edge in a social network'''

class Like(models.Model):
    '''Encapsulate the idea of a user liking a post'''

class Comment(models.Model):
    '''Encapsulate the idea of a comment on a post'''

