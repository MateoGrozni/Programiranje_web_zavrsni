from django.urls import path
from .views import MoodListView, home

urlpatterns = [
    path("", home, name="home"),
    path("moods/", MoodListView.as_view(), name="mood_list"),
]