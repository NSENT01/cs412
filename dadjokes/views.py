from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Joke, Picture
from random import randrange

# Create your views here.

def randomJoke(request):
    '''Display a random joke and picture'''

    template = 'dadjokes/random.html'
    jokes = list(Joke.objects.all())
    pictures = list(Picture.objects.all())
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

