from django.contrib import admin
from django.contrib import admin
from .models import Profile, MoodEntry, Tag

admin.site.register(Profile)
admin.site.register(MoodEntry)
admin.site.register(Tag)