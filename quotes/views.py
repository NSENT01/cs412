# File: views.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/18/2026
# Description: API for rendering HTML webpage

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time
# Create your views here.

# List of Kyrie Irving quotes
quotes = [
    '''No one is going to stop you from being yourself but yourself.''',
    '''It's okay to be human. I don't have to be perfect for anyone
    here, nor do I have to be perfect for the public. So I'm not here to dispel any perception. I'm just here to be myself.''',
    '''Everything has to be earned, not handed to you.''',
    '''The journey is the reward. Embrace the journey.''',
    '''Unleash everything you have and never look back. Never be afraid to be the best.''',
    '''Work hard, stay focused, and understand that nothing worth achieving comes easy.''',
    '''I think that the most important thing that I strive to live by is extremely by truth and by consistently giving others 
    the truth, without any judgement, without constraints, without anything extra except the understanding that I see you.''',
]

# List of Kyrie Irving image urls
image_urls = [
    '''https://wallpaperaccess.com/full/2135970.jpg''',
    '''https://cdn.nba.com/manage/2023/06/irving-claps063023.jpg''',
    '''https://wallpaperaccess.com/full/2135899.jpg''',
    '''https://cdn.nba.com/manage/2022/11/kyrie-irving-iso-1.jpg''',
    '''https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Kyrie_Irving_(51830909437)_(cropped).jpg/960px-Kyrie_Irving_(51830909437)_(cropped).jpg''',
    '''https://hips.hearstapps.com/hmg-prod/images/gettyimages-860566908.jpg?resize=980:*''',
    '''https://www.basketball-evolution.com/wp-content/uploads/2023/02/Kyrie-Irving-Dallas-Mavericks-NBA-news-1536x1015.jpg''',
]

def home(request):
    '''Respond the URL '', delegate task to a template'''
    # delegate to html template
    template = "quotes/quote.html"
    context = {
        "rquote": quotes[random.randrange(len(quotes))],
        "rimage": image_urls[random.randrange(len(image_urls))],
        "time": time.ctime(),
    }

    # return the rendered page
    return render(request, template, context)

def quote(request):
    '''Respond to the URL 'quote', delegate task to a template'''
    # delegate to html template
    template = "quotes/quote.html"

    # feed appropriate context for page rendering
    context = {
        "rquote": quotes[random.randrange(len(quotes))],
        "rimage": image_urls[random.randrange(len(image_urls))],
        "time": time.ctime(),
    }

    # return the rendered page
    return render(request, template, context)

def about(request):
    '''Respond to the URL 'about', delegate task to a template'''
    # delegate to html template
    template = "quotes/about.html"

    # feed appropriate context for page rendering
    context = {
        "time": time.ctime(),
        "img": image_urls[1],
    }

    # return the rendered page
    return render(request, template, context)

def show_all(request):
    '''Response to the URL 'show_all', delegate task to a template'''
    # delegate to html template
    template = "quotes/show_all.html"

    # feed appropriate context for page rendering
    context = {
        "quotes": list(zip(quotes, image_urls)),
        "time": time.ctime(),
    }

    # return the rendered page
    return render(request, template, context)