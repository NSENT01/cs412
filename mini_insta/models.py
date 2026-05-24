from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of a social media profile'''

    username = models.CharField(max_length=50, unique=True)
    display_name = models.TextField(max_length=50)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(max_length=100, blank=True)
    join_date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        '''Return the string representation of the Profile model'''
        return f'{self.username}'