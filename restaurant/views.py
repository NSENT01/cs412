# File: restaurant/views.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/20/2026
# Description: API for rendering HTML form and handling input data

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time
# Create your views here.

# list containing daily special items
specials = [
    "mochi",
    "chocolate cake",
    "cheescake",
    "boba"
]

def main(request):
    '''Respond the URL 'main', delegate task to a template'''
    # main.html path
    template = 'restaurant/main.html'

    # define context variable to be used by html template
    context = {
        "time": time.ctime(),
    }

    # render html file
    return render(request, template, context)

def order(request):
    # order.html path
    template = 'restaurant/order.html'

    # define context variables to be used by html template
    context = {
        "time": time.ctime(),
        "special": specials[random.randrange(len(specials))],
    }

    # render html file
    return render(request, template, context)

def confirmation(request):
    # confirmation.html path
    template = 'restaurant/confirmation.html'

    print(request.POST)

    # generate variables for context from request
    if request.POST:
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        flavor = request.POST["flavor"]

        toppings = []

        # iterate through options, check if they were selected, add to list
        for topping in ["oreos", "m&ms", "toffee", "gummies", "fruit"]:
            if topping in request.POST:
                toppings.append(request.POST[topping])

        if "special" in request.POST:
            special = request.POST["special"]
        else:
            special = ""

        special_request = request.POST["special_request"]

        # define context variables
        context = {
            "name": name,
            "phone": phone,
            "email": email,
            "flavor": flavor,
            "toppings": toppings,
            "special": special,
            "special_request": special_request,
            "time": time.ctime(),
            "ready_time": time.ctime(time.time() + random.randrange(1800, 3600))[11:16],
        }

    # render html file with context
    return render(request, template, context)