from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
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



