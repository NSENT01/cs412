# File: sipy/serializers.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 6/15/2026
# Description: Defining how incoming HTTP request are handled, serializing data, then defining outgoing requests

from rest_framework import serializers
from .models import *
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    '''Convert abstract python data on users to JSON for web communication'''

    class Meta:
        ''' Define the fields accepted by requests and extra kw arguments for password'''

        model = User
        fields = ['username', 'password', 'id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ProfileSerializer(serializers.ModelSerializer):
    '''Convert abstract python data objects into JSON to send to the front end'''

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        '''Define the fields from the model accepted by request and responses'''

        model = Profile
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'bio_text', 'profile_image']

    def create(self, validated_data):
        '''Override the create method to also create a user'''
        user_data = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password')
        }

        #create a user, then create profile and return profile
        user = User.objects.create_user(username=user_data['username'], password=user_data['password'])
        profile = Profile.objects.create(user=user, **validated_data)

        return profile

class ProfileUpdateSerializer(serializers.ModelSerializer):
    '''Convert profile update form data into an updated profile'''

    class Meta:
        '''Define the fields from the model accepted by request and responses'''
        model = Profile
        fields = ['first_name', 'last_name', 'bio_text', 'profile_image']

class ProfileGetSerializer(serializers.ModelSerializer):
    '''Convert abstract python data objects into JSON to send to the front end'''
    user = UserSerializer(read_only=True)

    # serializer method fields to append model method data to JSON response
    friend_rankings = serializers.SerializerMethodField()
    user_rankings = serializers.SerializerMethodField()
    num_rankings = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    num_followers = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()
    want_to_try = serializers.SerializerMethodField()

    class Meta:
        '''Define the fields from the model accepted by request and responses'''
        model = Profile
        fields = ['id', 'user', 'first_name', 'last_name', 'bio_text', 'profile_image', 'friend_rankings', 'user_rankings', 'num_rankings', 'num_followers', 'num_following', 'want_to_try']

    def get_profile_image(self, obj):
        '''Add the profile image to the JSON response'''
        request = self.context.get('request')

        # get profile image
        profile_image = obj.profile_image

        # standardized url so it can be referenced by frontend
        if not profile_image:
            return None

        if request:
            return request.build_absolute_uri(profile_image.url)

        return profile_image.url
    
    def get_num_followers(self, obj):
        '''Add the number of followers to the JSON response'''
        return len(obj.get_followers())
    
    def get_num_following(self, obj):
        '''Add the number of following to the JSON response'''
        return len(obj.get_following())

    def get_friend_rankings(self, obj):
        '''Add the rankings made by a users friends to the JSON response'''
        # use other serializer to JSONify data for response
        return RankingDisplaySerializer(obj.get_feed(), many=True, context=self.context).data
    
    def get_user_rankings(self, obj):
        '''Add the rankings made by the user to the JSON response'''
        # use other serializer to JSONify data for response
        return RankingDisplaySerializer(obj.get_user_rankings(), many=True, context=self.context).data

    def get_num_rankings(self, obj):
        '''Add the number of rankings made by a profile to the JSON response'''
        return obj.get_num_rankings()
    
    def get_want_to_try(self, obj):
        '''Add the want to try list to the JSON response'''
        # use other serializer to JSONify data for response
        return WantToTrySerializer(obj.get_want_to_try(), many=True, context=self.context).data


class CafeSerializer(serializers.ModelSerializer):
    '''Conver abstract python data on cafes to JSON to use for various database functions'''

    # serializer method fields to append model method data to JSON response
    average_rating = serializers.SerializerMethodField()
    num_rankings = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    friend_rankings = serializers.SerializerMethodField()
    friend_avg_ranking = serializers.SerializerMethodField()
    user_rankings = serializers.SerializerMethodField()
    user_avg_ranking = serializers.SerializerMethodField()

    class Meta:
        '''Define the fields from the model accepted by request and responses'''

        model = Cafe
        fields = ['id', 'placeId', 'name', 'address', 'latitude', 'longitude', 'website', 'phone_number', 'city', 'region', 'country', 'average_rating', 'num_rankings', 'images', 'friend_rankings', 'friend_avg_ranking', 'user_rankings', 'user_avg_ranking']

    def get_average_rating(self, obj):
        '''Add the average rating as an item in the JSON return object'''
        return obj.get_average_rating()
    
    def get_num_rankings(self, obj):
        '''Add the number of rankings as an item in the JSON return object'''
        return obj.get_num_rankings()
    
    def get_images(self, obj):
        '''Add the images that people have added for this cafe as an item in the JSON response object'''
        request = self.context.get('request')

        # exclude blank images because of model default
        images = Ranking.objects.filter(
            drink__cafe=obj
        ).exclude(
            image=''
        ).values_list('image', flat=True)

        # standardize url so frontend can reference
        if request:
            return [
                request.build_absolute_uri(settings.MEDIA_URL + image)
                for image in images
            ]

        return [
            settings.MEDIA_URL + image
            for image in images
        ]
    
    def get_friend_rankings(self, obj):
        '''Add the rankings made by a users friends to the JSON response'''

        # filter the following by the request user, and only use followed field values
        following = list(Follow.objects.filter(user=self.context['request'].user).values_list('followed', flat=True))
        
        # use other serializer to serialize data and return it
        return RankingDisplaySerializer(obj.get_friend_rankings(following), many=True, context=self.context,).data
    
    def get_friend_avg_ranking(self, obj):
        '''Add the average ranking of a users following to the JSON response'''

        # filter following by request user and only use followed field in list
        following = list(
            Follow.objects.filter(user=self.context['request'].user)
            .values_list('followed', flat=True)
        )

        # call method on object to get friend rankings
        friend_rankings = obj.get_friend_rankings(following)

        if len(friend_rankings) == 0:
            return None
        
        # compute friend average ranking
        return sum(ranking.score for ranking in friend_rankings) / len(friend_rankings)
    
    def get_user_rankings(self, obj):
        '''Add a users rankings to the JSON response'''
        # use other serializer to serializer data of different form 
        return RankingDisplaySerializer(obj.get_user_rankings(self.context['request'].user), many=True, context=self.context,).data
    
    def get_user_avg_ranking(self, obj):
        '''Add a users average ranking to the JSON response'''
        # call model method with input from request user
        user_rankings = obj.get_user_rankings(self.context['request'].user)
        if len(user_rankings) == 0:
            return None
        
        # compute users average ranking and return
        return sum(ranking.score for ranking in user_rankings) / len(user_rankings)

class RankingSerializer(serializers.ModelSerializer):
    '''Convert abstract python data on rankings to JSON for web communication'''

    # additional fields within nested foreign key
    drink_name = serializers.CharField(write_only=True)
    drink_category = serializers.CharField(write_only=True)
    cafe_id = serializers.CharField(write_only=True)

    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = Ranking
        fields = ['drink_name', 'drink_category', 'cafe_id', 'score', 'notes', 'image']

    def create(self, validated_data):
        '''Override the create method to define the user and drink fields'''
        drink_name = validated_data.pop('drink_name')
        cafe_id = validated_data.pop('cafe_id')
        defaults = validated_data.pop('drink_category')

        # get the cafe object with the request id
        cafe_object = Cafe.objects.get(
            placeId=cafe_id,
        )

        # get the drink object based on name or create it
        drink_object, created = Drink.objects.get_or_create(
            name=drink_name,
            cafe=cafe_object,
            defaults={"category": defaults}
        )

        # get user from request data
        user = self.context['request'].user

        # use the previously fetched cafe, and fetched or created drink to create or update a ranking
        ranking, created = Ranking.objects.update_or_create(user=user, drink=drink_object, defaults=validated_data)

        return ranking

class RankingDisplaySerializer(serializers.ModelSerializer):

    # additional fields for displaying a ranking, either from other models, or data from model methods
    drink_name = serializers.CharField(source='drink.name', read_only=True)
    drink_category = serializers.CharField(source='drink.category', read_only=True)
    image = serializers.SerializerMethodField()

    cafe_name = serializers.CharField(source='drink.cafe.name', read_only=True)

    liked_by_user = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    username = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = Ranking
        fields = [
            'id',
            'score',
            'notes',
            'image',

            'drink_name',
            'drink_category',

            'cafe_name',

            'liked_by_user',
            'num_likes',
            'num_comments',
            'comments',

            'username',
            'profile_image',
        ]

    def get_image(self, obj):
        '''Add the images that people have added for this cafe as an item in the JSON response object'''
        if not obj.image:
            return None
        
        request = self.context.get('request')

        # standardize image url so it can be referenced in frontend
        if request:
            return request.build_absolute_uri(obj.image.url)
                

        return obj.image.url
    
    def get_profile_image(self, obj):
        '''Add the profile image to the JSON response'''
        request = self.context.get('request')

        profile_image = obj.user.profile_user.profile_image

        # standardize image url so it can be referenced in frontend
        if not profile_image:
            return None

        if request:
            return request.build_absolute_uri(profile_image.url)

        return profile_image.url
    
    def get_liked_by_user(self, obj):
        '''Get boolean of if the user liked this ranking'''
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        # use exists orm method to return boolean of if the like object exists with the request user and ranking instance of the serializer
        return Like.objects.filter(
            user=request.user,
            ranking=obj,
        ).exists()

    def get_num_likes(self, obj):
        '''Get the number of likes'''
        return obj.likes.count()

    def get_num_comments(self, obj):
        '''Get the number of comments'''
        return obj.comments.count()
    
    def get_comments(self, obj):
        '''Get all the comments on a ranking, ordered by creation'''
        comments = obj.comments.select_related('user', 'user__profile_user').order_by('created_at')

        # serialize comment data with comment serializer
        return CommentSerializer(comments, many=True, context=self.context).data

            

class WantToTrySerializer(serializers.ModelSerializer):
    '''Convert abstract python data on places a user wants to try to JSON for web communication'''

    # additional id fields for incoming request, and cafe model field for outgoing responses
    cafeId = serializers.CharField(write_only=True)
    cafe = CafeSerializer(read_only=True)

    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = WantToTry
        fields = ['cafeId', 'cafe']

    def create(self, validated_data):
        '''Override the create method to define the user and cafe fields'''
        cafe_data = validated_data.pop('cafeId')

        # get user from request and cafe object based on cafeId from request
        user = self.context['request'].user
        cafe = Cafe.objects.get(placeId=cafe_data)

        # get the want to try object with this use and cafe, or create it
        wtt, created = WantToTry.objects.get_or_create(user=user, cafe=cafe, defaults={'user': user, 'cafe': cafe})
        return wtt
    
class FollowSerializer(serializers.ModelSerializer):
    '''Convert abstract python data types representing a follow edge into JSON to be sent across the web'''
    followed = serializers.CharField(write_only=True)

    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = Follow
        fields = ['followed']

    def validate(self, attrs):
        '''Override validate method to ensure user does not follow themselves'''
        followed_username = attrs.get('followed')
        request = self.context.get('request')

        # validate that the user is not following themselves
        if request and followed_username == request.user.username:
            raise serializers.ValidationError({'followed': 'You cannot follow yourself.'})

        return attrs

    def create(self, validated_data):
        '''Override create method to fetch required data to create this model instance'''
        followed_username = validated_data.pop('followed')

        # get user from context and followed with django orm
        user = self.context['request'].user
        followed = User.objects.get(username=followed_username)

        # get follow edge or create it
        follow, created = Follow.objects.get_or_create(
            user=user,
            followed=followed,
        )

        return follow

class LikeSerializer(serializers.ModelSerializer):
    '''Convert abstract python data on likes to JSON for web comm'''
    post = serializers.IntegerField(write_only=True)

    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = Like
        fields = ['post']

    def create(self, validated_data):
        '''override create to create an instance'''

        # get user from request context, ranking id from request data
        user = self.context['request'].user
        ranking_id = validated_data.pop('post')

        # get ranking associated with id using ORM
        ranking = Ranking.objects.get(id=ranking_id)

        # get or create like with these fields
        like, created = Like.objects.get_or_create(user=user, ranking=ranking)

        return like

class CommentSerializer(serializers.ModelSerializer):
    '''Convert abstract python data on comments to JSON for web comm'''

    # additional fields not on this model, or from this models methods
    post = serializers.IntegerField(write_only=True, required=False)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = Comment
        fields = [
            'id',
            'post',
            'text',
            'user_id',
            'username',
            'profile_image',
        ]

    def create(self, validated_data):
        '''Override create to attach the logged in user to the comment'''
        user = self.context['request'].user
        ranking_id = validated_data.pop('post', None)

        # require ranking id so object can be fetched
        if ranking_id is None:
            raise serializers.ValidationError({'post': 'This field is required.'})

        # try to get ranking object, if it does not exist then indicate no post exists for comment to be associated
        try:
            ranking = Ranking.objects.get(id=ranking_id)
        except Ranking.DoesNotExist:
            raise serializers.ValidationError({'post': 'No post exists with this id.'})

        # otherwise create the comment isntance with the appropriate fields
        return Comment.objects.create(user=user, ranking=ranking, **validated_data)

    def get_profile_image(self, obj):
        '''Get the profile image of the user who made the comment'''
        request = self.context.get('request')
        profile_image = obj.user.profile_user.profile_image

        # standardize url so it can be used in frontend
        if not profile_image:
            return None

        if request:
            return request.build_absolute_uri(profile_image.url)

        return profile_image.url

class ProfileSearchSerializer(serializers.ModelSerializer):
    '''Convert abstract python data on profiles to JSON for web responses for searching through profiles'''
    username = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = Profile
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'profile_image',
        ]

    def get_profile_image(self, obj):
        '''Get profile image of search results'''
        request = self.context.get('request')

        # standardize url so it can be used in frontend
        if not obj.profile_image:
            return None

        if request:
            return request.build_absolute_uri(obj.profile_image.url)

        return obj.profile_image.url
