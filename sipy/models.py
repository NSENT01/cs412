# File: sipy/models.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 6/15/2026
# Description: Defining the models used in our database

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of a user profile'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_user")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_image = models.ImageField(blank=True)
    bio_text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''return the string representation of a profile'''
        return f'{self.user.username}'

    def get_feed(self):
        '''Return the user's feed of rankings'''
        following = Follow.objects.filter(user=self.user)
        rankings = []

        for follow in following:
            rankings += list(Ranking.objects.filter(user=follow.followed))

        return sorted(rankings, key=lambda x: x.created_at, reverse=True)
    
    def get_following(self):
        '''Return the list of users that this user is following'''
        return Follow.objects.filter(user=self.user)
    
    def get_followers(self):
        '''Return the list of users that are following this user'''
        return Follow.objects.filter(followed=self.user)
    
    def get_personal_rankings(self):
        '''Return the user's personal rankings'''
        return Ranking.objects.filter(user=self.user)
    
    def get_want_to_try(self):
        '''Return the user's want to try list'''
        return WantToTry.objects.filter(user=self.user)
    
    def get_user_rankings(self):
        '''Return the users rankings'''
        return Ranking.objects.filter(user=self.user)
    
    def get_num_rankings(self):
        '''Return the number of rankings'''
        return len(self.get_user_rankings())
    
    def get_user_ranking_of_cafe(self, cafe):
        '''Return the user's ranking of a specific cafe'''
        rankings = Ranking.objects.filter(user=self.user, drink__cafe=cafe)
        if not rankings:
            return None
        return sum(ranking.score for ranking in rankings) / len(rankings)
    
    def get_following_ranking_of_cafe(self, cafe):
        '''Return the user's follower's ranking of a specific cafe'''
        followers = Follow.objects.filter(user=self.user)
        rankings = []
        for follow in followers:
            rankings += list(Ranking.objects.filter(user=follow.followed, drink__cafe=cafe))
        if not rankings:
            return None
        return sum(ranking.score for ranking in rankings) / len(rankings)


class Cafe(models.Model):
    '''Encapsulate the idea of a cafe item'''
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    placeId = models.CharField(max_length=200, unique=True)
    website = models.URLField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        '''return the string representation of a cafe'''
        return f'{self.name}'

    def get_average_rating(self):
        '''Return the average rating for this cafe'''
        rankings = Ranking.objects.filter(drink__cafe=self)
        if not rankings:
            return None
        return sum(rating.score for rating in rankings) / len(rankings)
    
    def get_num_rankings(self):
        '''Return the number of rankings for this cafe'''
        return Ranking.objects.filter(drink__cafe=self).count()
    
    def get_images(self):
        '''Return the images uploaded by people of this cafe'''
        return Ranking.objects.filter(drink__cafe=self).values_list('image', flat=True)
    
    def get_friend_rankings(self, users):
        '''Return the rankings made by a users friends'''
        rankings = []

        for user in users:
            rankings += list(Ranking.objects.filter(user=user, drink__cafe=self))

        return rankings
    
    def get_user_rankings(self, user):
        '''Return the users rankings'''
        rankings = list(Ranking.objects.filter(user=user, drink__cafe=self))

        return rankings


class Drink(models.Model):
    '''Encapsulate the idea of a drink from a cafe'''
    name = models.CharField(max_length=100)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="drinks")

    drink_choices = {
        "Coffee": "Coffee",
        "Matcha": "Matcha",
        "Tea": "Tea",
        "Boba": "Boba",
        "Juice": "Juice",
        "Smoothies": "Smoothies",
        "Soda": "Soda",
        "Alcohol": "Alcohol",
        "Other": "Other"
    }

    category = models.CharField(max_length=50, default="Coffee", choices=drink_choices)

    def __str__(self):
        '''return the string representation of a drink'''
        return f'{self.name} from {self.cafe}'

class Ranking(models.Model):
    '''Encapsulate the idea of a drink ranking'''
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, related_name="rankings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rankings")
    score = models.DecimalField(max_digits=3, decimal_places=1)
    notes = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        '''Define the unqiue constraints of the model for security'''
        constraints = [
            models.UniqueConstraint(fields=['user', 'drink'], name='unique_user_ranking')
        ]

    def __str__(self):
        '''return the string representation of a ranking'''
        return f'{self.user} gave {self.drink} a {self.score}'


class WantToTry(models.Model):
    '''Encapsulate the idea of a want to try list'''
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="want_to_try")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="want_to_try")

    class Meta:
        '''Define the unqiue constraints of the model for security'''
        constraints = [
            models.UniqueConstraint(fields=['user', 'cafe'], name='unique_user_bookmark')
        ]

    def __str__(self):
        '''return the string representation of wanttotry object'''
        return f'{self.user} wants to try {self.cafe}'

class Follow(models.Model):
    '''Encapsulate the idea of a follow edge in a social network'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        '''Define the unqiue constraints of the model for security'''
        constraints = [
            models.UniqueConstraint(fields=['user', 'followed'], name='unique_user_follow')
        ]

    def __str__(self):
        '''return string representation of follow'''
        return f'{self.user} followed {self.followed}'

class Like(models.Model):
    '''Encapsulate the idea of a user liking a post'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        '''Define the unqiue constraints of the model for security'''
        constraints = [
            models.UniqueConstraint(fields=['user', 'ranking'], name='unique_user_ranking_like')
        ]

    def __str__(self):
        '''return string representation of like'''
        return f'{self.user} liked {self.ranking}'

class Comment(models.Model):
    '''Encapsulate the idea of a comment on a post'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''return string representation of comment'''
        return f'{self.user} commented ({self.text}) on {self.ranking}'

