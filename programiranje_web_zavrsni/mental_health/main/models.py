from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    date_of_birth = models.DateField(null=True, blank=True)
    timezone = models.CharField(max_length=64, default="Europe/Zagreb")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MoodEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mood_entries",
    )
    mood = models.PositiveSmallIntegerField()
    stress = models.PositiveSmallIntegerField()
    note = models.TextField(blank=True)

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="mood_entries",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} mood={self.mood} stress={self.stress} ({self.created_at:%Y-%m-%d})"