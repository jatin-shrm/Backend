from django.contrib import admin
from .models import UserProfile, UserImage

admin.site.register(UserProfile)
admin.site.register(UserImage)