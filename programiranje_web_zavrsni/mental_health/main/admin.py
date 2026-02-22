from django.contrib import admin
from django.contrib import admin
from .models import MoodEntry, Tag

admin.site.register(MoodEntry)
admin.site.register(Tag)