# File: dadjokes/admin.py
# Author: Nithin Senthilvel (nsent01@bu.edu), 06/10/2026
# Description: Register models in admin

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Joke)
admin.site.register(Picture)
