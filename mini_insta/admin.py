# File: mini_insta/models.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 5/22/2026
# Description: Register the model to be used in admin

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follower)
admin.site.register(Like)
admin.site.register(Comment)