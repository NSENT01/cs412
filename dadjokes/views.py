# File: dadjokes/views.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 06/10/2026
# Description: Define the api views and the web page views

from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Joke, Picture
from random import randrange
from rest_framework import generics
from .serializers import *
# Create your views here.

def randomJoke(request):
    '''Display a random joke and picture'''

    template = 'dadjokes/random.html'
    jokes = list(Joke.objects.all())
    pictures = list(Picture.objects.all())

    # return a random joke and picture from after retrieving all of them
    context = {
        'joke': jokes[randrange(0, len(jokes))],
        'picture': pictures[randrange(0, len(pictures))],
    }

    return render(request, template, context)

class JokeDetailView(DetailView):
    '''Display one joke'''

    model = Joke
    template_name = "dadjokes/joke.html"
    context_object_name = 'joke'

class JokeListView(ListView):
    '''Display all jokes'''

    model = Joke
    template_name = "dadjokes/all_jokes.html"
    context_object_name = 'jokes'

class PictureDetailView(DetailView):
    '''Display a picture'''

    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'

class PictureListView(ListView):
    '''Display all picture'''

    model = Picture
    template_name = 'dadjokes/all_pictures.html'
    context_object_name = 'pictures'

class JokeListCreateView(generics.ListCreateAPIView):
    '''Return all jokes in JSON'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListCreateView(generics.ListCreateAPIView):
    '''Return all pictures in JSON'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class JokeRetrieveView(generics.RetrieveAPIView):
    '''Return one joke as JSON, support update and delete'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer
    lookup_field = 'pk'

class PictureRetrieveView(generics.RetrieveAPIView):
    '''Return one picture as JSON, support update and delete'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    lookup_field = 'pk'

class RandomJokeRetrieveView(generics.RetrieveAPIView):
    '''Return a random joke as JSON'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

    def get_object(self):
        '''Override get_object method to return a random Joke object'''
        joke = Joke.objects.order_by('?').first()
        return joke
    
class RandomPictureRetrieveView(generics.RetrieveAPIView):
    '''Return a random picture as JSON'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def get_object(self):
        '''Override get_object method to return a random Picture object'''
        picture = Picture.objects.order_by('?').first()
        return picture