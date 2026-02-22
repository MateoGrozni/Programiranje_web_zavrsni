from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import MoodEntryForm
from .models import MoodEntry


def home(request):
    return redirect("dashboard" if request.user.is_authenticated else "login")


class MoodListView(LoginRequiredMixin, ListView):
    template_name = "main/mood_list.html"
    context_object_name = "moods"
    login_url = "login"

    def get_queryset(self):
        q = (self.request.GET.get("q") or "").strip()

        qs = (
            MoodEntry.objects
            .filter(user=self.request.user)
            .prefetch_related("tags")
            .order_by("-id")
        )

        if q:
            qs = qs.filter(Q(note__icontains=q) | Q(tags__name__icontains=q)).distinct()

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = (self.request.GET.get("q") or "").strip()
        return ctx


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
    form_class = MoodEntryForm  # bolje nego fields=[...] jer zadržavaš isti UX/validaciju
    template_name = "main/mood_form.html"
    success_url = reverse_lazy("mood_list")

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user)


class MoodDeleteView(LoginRequiredMixin, DeleteView):
    model = MoodEntry
    template_name = "main/mood_confirm_delete.html"
    success_url = reverse_lazy("mood_list")

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user)


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # auto-login nakon registracije
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "main/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["moods"] = (
            MoodEntry.objects
            .filter(user=self.request.user)
            .prefetch_related("tags")
            .order_by("-id")[:10]
        )
        return ctx