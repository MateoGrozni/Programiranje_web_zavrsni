from django.contrib import admin
from django.contrib import admin
from .models import Profile, MoodEntry, JournalEntry, Tag

admin.site.register(Profile)
admin.site.register(MoodEntry)
admin.site.register(JournalEntry)
admin.site.register(Tag)