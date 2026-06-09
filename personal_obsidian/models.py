# File: personal_obsidian/models.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 6/08/2026
# Description: Defining the models used in our database

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of a profile and user in the app'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Node(models.Model):
    '''Encapsulate the idea of a node in a knowledge graph'''
    concept = models.TextField(blank=True)
    content = models.FileField(blank=True)

class Root(models.Model):
    '''Encapsulate the idea of a root node for a knowledge graph'''
    node = models.ForeignKey(Node, on_delete=models.CASCADE)

class Edge(models.Model):
    '''Encapsulate the idea of core display nodes in the knowledge graph'''
    start = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="start")
    destination = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="destination")

class Like(models.Model):
    '''Encapsulate the idea of liking a knowledge graph'''

class Follower(models.Model):
    '''Encapsulate the idea of a follower'''