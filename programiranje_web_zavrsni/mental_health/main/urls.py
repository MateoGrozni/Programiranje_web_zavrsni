from django.urls import path

from .views import (
    DashboardView,
    MeditationCreateView,
    MeditationDeleteView,
    MeditationListView,
    MoodCreateView,
    MoodDeleteView,
    MoodListView,
    MoodUpdateView,
    home,
)

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    path("moods/", MoodListView.as_view(), name="mood_list"),
    path("moods/new/", MoodCreateView.as_view(), name="mood_create"),
    path("moods/<int:pk>/edit/", MoodUpdateView.as_view(), name="mood_edit"),
    path("moods/<int:pk>/delete/", MoodDeleteView.as_view(), name="mood_delete"),

    path("meditations/", MeditationListView.as_view(), name="meditation_list"),
    path("meditations/new/", MeditationCreateView.as_view(), name="meditation_create"),
    path("meditations/<int:pk>/delete/", MeditationDeleteView.as_view(), name="meditation_delete"),
]