from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *
from django.db.models import Q, Avg, Count
from django.views.generic import ListView


# Create your views here.

class SipyModelListView(ListView):
    '''Base list view for simple web pages that display sipy model data'''
    template_name = 'sipy/model_list.html'
    context_object_name = 'objects'
    fields = []
    page_title = ''

    def get_queryset(self):
        '''Return objects with default ordering for display'''
        return self.model.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        '''Add display metadata for the shared list template'''
        context = super().get_context_data(**kwargs)
        rows = []

        for obj in context['objects']:
            values = []

            for field in self.fields:
                value = getattr(obj, field)
                values.append(value)

            rows.append(values)

        context['fields'] = self.fields
        context['rows'] = rows
        context['page_title'] = self.page_title
        return context


class ProfileListView(SipyModelListView):
    '''Display all profiles'''
    model = Profile
    page_title = 'Profiles'
    fields = ['id', 'user', 'first_name', 'last_name', 'bio_text', 'profile_image', 'timestamp']


class CafeListView(SipyModelListView):
    '''Display all cafes'''
    model = Cafe
    page_title = 'Cafes'
    fields = ['id', 'name', 'address', 'latitude', 'longitude', 'placeId', 'city', 'region', 'country']


class DrinkListView(SipyModelListView):
    '''Display all drinks'''
    model = Drink
    page_title = 'Drinks'
    fields = ['id', 'name', 'cafe', 'category']


class RankingListView(SipyModelListView):
    '''Display all rankings'''
    model = Ranking
    page_title = 'Rankings'
    fields = ['id', 'user', 'drink', 'score', 'notes', 'image', 'created_at']


class WantToTryListView(SipyModelListView):
    '''Display all want-to-try records'''
    model = WantToTry
    page_title = 'Want To Try'
    fields = ['id', 'user', 'cafe']


class FollowListView(SipyModelListView):
    '''Display all follow records'''
    model = Follow
    page_title = 'Follows'
    fields = ['id', 'user', 'followed']


class LikeListView(SipyModelListView):
    '''Display all like records'''
    model = Like
    page_title = 'Likes'
    fields = ['id', 'user', 'ranking', 'created_at']


class CommentListView(SipyModelListView):
    '''Display all comment records'''
    model = Comment
    page_title = 'Comments'
    fields = ['id', 'user', 'ranking', 'text', 'created_at']

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

class UpdateProfileView(generics.UpdateAPIView):
    '''Inherit from UpdateAPIView to update the logged in user's profile'''
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['patch']

    def get_object(self):
        '''Define the profile being updated'''
        return Profile.objects.get(user=self.request.user)

class DeleteProfileView(generics.DestroyAPIView):
    '''Inherit from DestroyAPIView to delete the logged in user's profile'''
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''Define the profile being deleted'''
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
    serializer_class = RankingDisplaySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''Override method to retrieve an instance based on request data'''
        return get_object_or_404(Ranking, id=self.request.GET['id'])
    
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

    def get_object(self):
        '''Define the follow edge to be deleted'''
        return Follow.objects.get(user=self.request.user, followed__username=self.request.GET['followed'])
    
class GetFollowView(generics.RetrieveAPIView):
    '''Inherit from retrieve api generic to get a follow edge'''
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''Define the follow edge being fetched'''
        return Follow.objects.get(user=self.request.user, followed__username=self.request.GET['followed'])
    
class GetFollowingView(generics.ListAPIView):
    '''Inherit from the list api view to get a users following'''
    serializer_class = ProfileGetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Profile.objects.filter(
            user__followers__user=self.request.user
        )
    
class GetFollowersView(generics.ListAPIView):
    '''Inherit from the list api view to get a users followers'''
    serializer_class = ProfileGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(
            user__following__followed=self.request.user
        )

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

class GetTasteProfileView(generics.GenericAPIView):
    '''Return the logged in user's ranking summary grouped by cafe location'''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''Return cafe counts and aggregate ratings by country and city'''
        username = request.GET.get('username')
        user = request.user

        if username:
            user = get_object_or_404(User, username=username)

        user_rankings = Ranking.objects.filter(user=user)

        countries = user_rankings.values(
            'drink__cafe__country'
        ).annotate(
            num_cafes=Count('drink__cafe', distinct=True),
            aggregate_rating=Avg('score'),
        ).order_by('drink__cafe__country')

        cities = user_rankings.values(
            'drink__cafe__city'
        ).annotate(
            num_cafes=Count('drink__cafe', distinct=True),
            aggregate_rating=Avg('score'),
        ).order_by('drink__cafe__city')

        return Response({
            'countries': [
                {
                    'country': item['drink__cafe__country'] or 'Unknown',
                    'num_cafes': item['num_cafes'],
                    'aggregate_rating': item['aggregate_rating'],
                }
                for item in countries
            ],
            'cities': [
                {
                    'city': item['drink__cafe__city'] or 'Unknown',
                    'num_cafes': item['num_cafes'],
                    'aggregate_rating': item['aggregate_rating'],
                }
                for item in cities
            ],
        })

class CreateWantToTryView(generics.CreateAPIView):
    '''Inherit from CreatAPIView to create a want to try item'''
    serializer_class = WantToTrySerializer
    permission_classes = [IsAuthenticated]

class GetWantToTryView(generics.RetrieveAPIView):
    '''Inherit from the RetrieveAPIView to get a favorited cafe'''
    serializer_class = WantToTrySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''Define the object returned on GET'''
        return WantToTry.objects.get(cafe__placeId=self.request.GET['cafeId'])

class DeleteWantToTryView(generics.DestroyAPIView):
    '''Inherit from DestroyAPIView to delete a favorite'''
    serializer_class = WantToTrySerializer
    permission_classes = [IsAuthenticated]
    queryset = WantToTry.objects.all()

    def get_object(self):
        '''Define object sent to serializer for deletion'''
        return WantToTry.objects.get(user=self.request.user, cafe__placeId=self.request.GET['cafeId'])

class ProfileSearchView(generics.ListAPIView):
    serializer_class = ProfileSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.GET.get('q', '')

        if not query:
            return Profile.objects.none()

        return Profile.objects.filter(
            Q(user__username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(
            user=self.request.user
        )
    
class CreateLikeView(generics.CreateAPIView):
    '''Inherit from create generic api to create a like'''
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

class DeleteLikeView(generics.DestroyAPIView):
    '''Inherit from delete generic view to delete a like'''
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''get the object to be deleted by serializer'''
        ranking_id = self.request.GET.get('post')
        return Like.objects.get(user=self.request.user, ranking__id=ranking_id)

class CreateCommentView(generics.CreateAPIView):
    '''Inherit from create generic api to create a comment'''
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class DeleteCommentView(generics.DestroyAPIView):
    '''Inherit from delete generic view to delete a comment'''
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''Get the logged in user's comment to be deleted'''
        return get_object_or_404(Comment, id=self.request.GET.get('id'), user=self.request.user)
