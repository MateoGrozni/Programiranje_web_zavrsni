from django.http import HttpResponse
from django.views.generic import ListView
from .models import MoodEntry

def home(request):
    return HttpResponse("Mental health tracker radi ✅")

class MoodListView(ListView):
    model = MoodEntry
    template_name = "main/mood_list.html"
    context_object_name = "moods"

