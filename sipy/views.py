from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from .models import *
from .serializers import *


# Create your views here.

class CreateAccountView(generics.CreateAPIView):
    '''Inherit from CreateAPI to register a new user'''
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]


