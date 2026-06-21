from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Profile)
admin.site.register(Cafe)
admin.site.register(Drink)
admin.site.register(Ranking)
admin.site.register(WantToTry)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Comment)
