from django.contrib import admin
from django.contrib import admin
from .models import MoodEntry, Tag, MeditationSession

admin.site.register(MoodEntry)
admin.site.register(Tag)
admin.site.register(MeditationSession)