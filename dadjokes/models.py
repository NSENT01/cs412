from django.db import models

# Create your models here.

class Joke(models.Model):
    '''Encapsulate the idea of a joke as a data model'''
    text = models.TextField(blank=True)
    name = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}: {self.pk}'

class Picture(models.Model):
    '''Encapsulate the idea of a picture as a data model'''
    image_url = models.URLField(blank=True)
    name = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}: {self.pk}'