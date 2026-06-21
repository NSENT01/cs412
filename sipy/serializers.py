

from rest_framework import serializers
from .models import *
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    '''Convert abstract python data on users to JSON for web communication'''
    class Meta:
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
        model = Profile
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'bio_text', 'profile_image']

    def create(self, validated_data):
        '''Override the create method to also create a user'''
        user_data = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password')
        }
        user = User.objects.create_user(username=user_data['username'], password=user_data['password'])
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

class ProfileGetSerializer(serializers.ModelSerializer):
    '''Convert abstract python data objects into JSON to send to the front end'''
    user = UserSerializer(read_only=True)
    friend_rankings = serializers.SerializerMethodField()
    user_rankings = serializers.SerializerMethodField()
    num_rankings = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    num_followers = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'first_name', 'last_name', 'bio_text', 'profile_image', 'friend_rankings', 'user_rankings', 'num_rankings', 'num_followers', 'num_following']

    def get_profile_image(self, obj):
        '''Add the profile image to the JSON response'''
        request = self.context.get('request')

        profile_image = obj.profile_image

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
        
        return RankingDisplaySerializer(obj.get_feed(), many=True, context=self.context).data
    
    def get_user_rankings(self, obj):
        '''Add the rankings made by the user to the JSON response'''

        return RankingDisplaySerializer(obj.get_user_rankings(), many=True, context=self.context).data

    def get_num_rankings(self, obj):
        '''Add the number of rankings made by a profile to the JSON response'''

        return obj.get_num_rankings()


class CafeSerializer(serializers.ModelSerializer):
    '''Conver abstract python data on cafes to JSON to use for various database functions'''

    average_rating = serializers.SerializerMethodField()
    num_rankings = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    friend_rankings = serializers.SerializerMethodField()
    friend_avg_ranking = serializers.SerializerMethodField()
    user_rankings = serializers.SerializerMethodField()
    user_avg_ranking = serializers.SerializerMethodField()

    class Meta:
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

        images = Ranking.objects.filter(
            drink__cafe=obj
        ).exclude(
            image=''
        ).values_list('image', flat=True)

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
        following = list(Follow.objects.filter(user=self.context['request'].user).values_list('followed', flat=True))
        
        return RankingDisplaySerializer(obj.get_friend_rankings(following), many=True, context=self.context,).data
    
    def get_friend_avg_ranking(self, obj):
        '''Add the average ranking of a users following to the JSON response'''
        following = list(
            Follow.objects.filter(user=self.context['request'].user)
            .values_list('followed', flat=True)
        )

        friend_rankings = obj.get_friend_rankings(following)

        if len(friend_rankings) == 0:
            return None
        return sum(ranking.score for ranking in friend_rankings) / len(friend_rankings)
    
    def get_user_rankings(self, obj):
        '''Add a users rankings to the JSON response'''
        return RankingDisplaySerializer(obj.get_user_rankings(self.context['request'].user), many=True, context=self.context,).data
    
    def get_user_avg_ranking(self, obj):
        '''Add a users average ranking to the JSON response'''
        user_rankings = obj.get_user_rankings(self.context['request'].user)
        if len(user_rankings) == 0:
            return None
        return sum(ranking.score for ranking in user_rankings) / len(user_rankings)

class DrinkSerializer(serializers.ModelSerializer):
    '''Convert abstract python data on drinks to JSON to user for various database functions'''
    cafe = CafeSerializer()

    class Meta:
        model = Drink
        fields = ['id', 'name', 'cafe', 'category']

    def create(self, validated_data):
        '''Override the create method to define the cafe field'''
        cafe_data = validated_data.pop('cafe')

        cafe_object, created = Cafe.objects.get_or_create(
            placeId=cafe_data['placeId'],
            defaults=cafe_data
        )

        drink, created = Drink.objects.get_or_create(cafe=cafe_object, name=validated_data.pop('name'), defaults=validated_data)
        return drink
        


class RankingSerializer(serializers.ModelSerializer):
    '''Convert abstract python data on rankings to JSON for web communication'''
    drink_name = serializers.CharField(write_only=True)
    drink_category = serializers.CharField(write_only=True)
    cafe_id = serializers.CharField(write_only=True)

    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = Ranking
        fields = ['id', 'drink_name', 'drink_category', 'cafe_id', 'score', 'notes', 'image', 'created_at']

    def create(self, validated_data):
        '''Override the create method to define the user and drink fields'''
        drink_name = validated_data.pop('drink_name')
        cafe_id = validated_data.pop('cafe_id')
        defaults = validated_data.pop('drink_category')

        cafe_object = Cafe.objects.get(
            placeId=cafe_id,
        )

        drink_object, created = Drink.objects.get_or_create(
            name=drink_name,
            cafe=cafe_object,
            defaults={"category": defaults}
        )

        user = self.context['request'].user

        ranking, created = Ranking.objects.update_or_create(user=user, drink=drink_object, defaults=validated_data)

        return ranking

class RankingDisplaySerializer(serializers.ModelSerializer):
    drink_name = serializers.CharField(source='drink.name', read_only=True)
    drink_category = serializers.CharField(source='drink.category', read_only=True)
    image = serializers.SerializerMethodField()

    cafe_name = serializers.CharField(source='drink.cafe.name', read_only=True)
    cafe_place_id = serializers.CharField(source='drink.cafe.placeId', read_only=True)

    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Ranking
        fields = [
            'id',
            'score',
            'notes',
            'image',
            'created_at',

            'drink_name',
            'drink_category',

            'cafe_name',
            'cafe_place_id',

            'user_id',
            'username',
            'profile_image',
        ]

    def get_image(self, obj):
        '''Add the images that people have added for this cafe as an item in the JSON response object'''
        if not obj.image:
            return None
        
        request = self.context.get('request')

        if request:
            return request.build_absolute_uri(obj.image.url)
                

        return obj.image.url
    
    def get_profile_image(self, obj):
        '''Add the profile image to the JSON response'''
        request = self.context.get('request')

        profile_image = obj.user.profile_user.profile_image

        if not profile_image:
            return None

        if request:
            return request.build_absolute_uri(profile_image.url)

        return profile_image.url

            

class WantToTrySerializer(serializers.ModelSerializer):
    '''Convert abstract python data on places a user wants to try to JSON for web communication'''
    cafe = CafeSerializer()

    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = WantToTry
        fields = ['cafe']

    def create(self, validated_data):
        '''Override the create method to define the user and cafe fields'''
        cafe_data = validated_data.pop('cafe')

        user = self.context['request'].user
        cafe = Cafe.objects.get(placeId=cafe_data['placeId'])

        wtt = WantToTry.objects.create(user=user, cafe=cafe)
        return wtt
    
class FollowSerializer(serializers.ModelSerializer):
    '''Convert abstract python data on follow edges to JSON for web comm'''
    user = UserSerializer()
    followed = UserSerializer()

    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = Follow
        fields = ['user', 'followed']

class LikeSerializer(serializers.ModelSerializer):
    '''Convert abstract python data on likes to JSON for web comm'''
    user = UserSerializer()
    ranking = RankingSerializer()

    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = Like
        fields = ['user', 'ranking', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    '''Convert abstract python data on comments to JSON for web comm'''
    user = UserSerializer()
    ranking = RankingSerializer()
    
    class Meta:
        '''Define the model to write and read from and the values to write and read'''
        model = Comment
        fields = ['user', 'ranking', 'text', 'created_at']

