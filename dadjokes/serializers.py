from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    '''Convert model data to HTTP valid format'''

    class Meta:
        '''Define the attributes and model'''
        model = Joke
        fields = ['id', 'text', 'name', 'timestamp']
        read_only_fields = ["id", "timestamp"]

class PictureSerializer(serializers.ModelSerializer):
    '''Convert model data to HTTP valid format'''

    class Meta:
        '''Define the attributes and model'''
        model = Picture
        fields = ['id', 'image_url', 'name', 'timestamp']
        read_only_fields = ["id", "timestamp"]