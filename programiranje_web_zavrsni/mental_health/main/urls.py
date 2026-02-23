from django.urls import path
from .views import home, MoodListView, MoodCreateView, MoodUpdateView, MoodDeleteView, DashboardView, MeditationListView, MeditationCreateView, MeditationDeleteView

urlpatterns = [
    path("", home, name="home"),
    path("moods/", MoodListView.as_view(), name="mood_list"),
    path("moods/new/", MoodCreateView.as_view(), name="mood_create"),
    path("moods/<int:pk>/edit/", MoodUpdateView.as_view(), name="mood_edit"),
    path("moods/<int:pk>/delete/", MoodDeleteView.as_view(), name="mood_delete"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("meditations/", MeditationListView.as_view(), name="meditation_list"),
    path("meditations/new/", MeditationCreateView.as_view(), name="meditation_create"),
    path("meditations/<int:pk>/delete/", MeditationDeleteView.as_view(), name="meditation_delete"),
]