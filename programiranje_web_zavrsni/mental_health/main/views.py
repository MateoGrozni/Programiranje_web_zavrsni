from django.http import HttpResponse
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import MoodEntry, Tag
from django.contrib.auth.forms import UserCreationForm
from .forms import MoodEntryForm

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")

class MoodListView(LoginRequiredMixin, ListView):
    model = MoodEntry
    template_name = "main/mood_list.html"
    context_object_name = "moods"
    login_url = "login"

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user).order_by("-id")

class MoodCreateView(LoginRequiredMixin, CreateView):
    model = MoodEntry
    form_class = MoodEntryForm
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

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("mood_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # auto-login nakon registracije
        return response

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "main/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        q = (self.request.GET.get("q") or "").strip()
        user = self.request.user

        moods_qs = MoodEntry.objects.filter(user=user).order_by("-id")
        tags_qs = Tag.objects.all().order_by("name")

        if q:
            moods_qs = moods_qs.filter(note__icontains=q)
            tags_qs = tags_qs.filter(name__icontains=q)

        ctx["q"] = q
        ctx["moods"] = moods_qs[:10]   

        return ctx