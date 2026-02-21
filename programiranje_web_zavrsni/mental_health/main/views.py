from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from .models import MoodEntry

def home(request):
    return HttpResponse("Mental health tracker radi ✅")

class MoodListView(ListView):
    model = MoodEntry
    template_name = "main/mood_list.html"
    context_object_name = "moods"

class MoodCreateView(LoginRequiredMixin, CreateView):
    model = MoodEntry
    fields = ["mood", "stress", "note"]
    template_name = "main/mood_form.html"
    success_url = reverse_lazy("mood_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)