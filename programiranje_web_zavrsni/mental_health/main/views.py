from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import MoodEntry

def home(request):
    return HttpResponse("Mental health tracker radi ✅")

class MoodListView(LoginRequiredMixin, ListView):
    model = MoodEntry
    template_name = "main/mood_list.html"
    context_object_name = "moods"
    login_url = "login"

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user).order_by("-id")

class MoodCreateView(LoginRequiredMixin, CreateView):
    model = MoodEntry
    fields = ["mood", "stress", "note"]
    template_name = "main/mood_form.html"
    success_url = reverse_lazy("mood_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MoodUpdateView(LoginRequiredMixin, UpdateView):
    model = MoodEntry
    fields = ["mood", "stress", "note"]
    template_name = "main/mood_form.html"
    success_url = reverse_lazy("mood_list")

    def get_queryset(self):
        # sprječava edit tuđih unosa
        return MoodEntry.objects.filter(user=self.request.user)


class MoodDeleteView(LoginRequiredMixin, DeleteView):
    model = MoodEntry
    template_name = "main/mood_confirm_delete.html"
    success_url = reverse_lazy("mood_list")

    def get_queryset(self):
        # sprječava delete tuđih unosa
        return MoodEntry.objects.filter(user=self.request.user)