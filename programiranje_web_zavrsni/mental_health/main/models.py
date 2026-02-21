from django.db import models
from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    timezone = models.CharField(max_length=64, default="Europe/Zagreb")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


class MoodEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mood_entries")
    mood = models.PositiveSmallIntegerField()    # 1-10
    stress = models.PositiveSmallIntegerField()  # 1-10
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} mood={self.mood} stress={self.stress} ({self.created_at:%Y-%m-%d})"


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="journal_entries")
    title = models.CharField(max_length=120)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name="journal_entries")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.title}"
