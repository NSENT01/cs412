from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework import mixins
from .models import *
from .serializers import *


# Create your views here.

class CreateAccountView(generics.CreateAPIView):
    '''Inherit from CreateAPI to register a new user'''
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]


class GetSingleProfileView(generics.RetrieveAPIView):
    '''Inherit from RetrieveAPIView to get a single profile'''
    serializer_class = ProfileGetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
class GetOtherProfileView(generics.RetrieveAPIView):
    '''Inherit from RetrieveAPIView to get a single other profile'''
    serializer_class = ProfileGetSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''Define the object that is retrieved and sent in JSON response'''
        return Profile.objects.get(user__username=self.request.GET['id'])
    
class GetCafeView(generics.RetrieveAPIView):
    '''Inherit from RetrieveAPIView to get a single cafes details'''
    serializer_class = CafeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''Define the object that will be returned with a get request'''
        return Cafe.objects.get(placeId=self.request.GET['cafe'])
    
class CreateCafeView(generics.CreateAPIView):
    '''Inherit from CreateAPIView to create a cafe in the database'''
    serializer_class = CafeSerializer
    permission_classes = [IsAuthenticated]
    
class GetDrinkView(generics.RetrieveAPIView):
    '''Inherit from RetrieveAPIView to get a single drinks details'''
    serializer_class = DrinkSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''Define the object that will be returned with a get request'''
        return Drink.objects.get(cafe__placeId=self.request.GET['cafe'], name=self.request.GET['name'])
    
class CreateDrinkView(generics.CreateAPIView):
    '''Inherit from CreateAPIView to create an instance of a drink'''
    serializer_class = DrinkSerializer
    permission_classes = [IsAuthenticated]

class GetRankingView(generics.RetrieveAPIView):
    '''Inherit from RetrieveAPIView to get a single ranking'''
    serializer_class = RankingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''Override method to retrieve an instance based on request data'''
        return Ranking.objects.get(user=self.request.user, drink__id=self.request.GET['drink'])
    
class CreateRankingView(generics.CreateAPIView):
    '''Inherit from CreateAPIView to create an instance of a ranking'''
    serializer_class = RankingSerializer
    permission_classes = [IsAuthenticated]
    
class DestroyRankingView(generics.DestroyAPIView):
    '''Inherit from DestroyAPIView to get a delete an instance of Ranking'''
    serializer_class = RankingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Ranking.objects.all()

    def get_object(self):
        '''Define the object to be destroyed'''
        return Ranking.objects.get(id=self.request.GET['id'], user=self.request.user)
    
class CreateFollowView(generics.CreateAPIView):
    '''Inherit from CreateAPIView to create a follow edge'''
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

class DestroyFollowView(generics.DestroyAPIView):
    '''Inherit from DestroyAPIView to delete a follow edge'''
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

class GetAllProfilesView(generics.ListAPIView):
    '''Inherit from ListAPIView to retrieve all profile data'''
    serializer_class = ProfileGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''Override queryset method to return profiles sorted by number of rankings'''
        profiles = list(Profile.objects.all())
        profiles.sort(
            key=lambda profile: profile.get_num_rankings(),
            reverse=True
        )
        return profiles

        
