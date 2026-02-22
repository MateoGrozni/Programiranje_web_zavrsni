from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        # mala normalizacija imena taga
        self.name = self.name.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MoodEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mood_entries",
    )

    # skala 1–10 (promijeni ako želiš 1–5)
    mood = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    stress = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

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
        return (
            f"{self.user.username} "
            f"mood={self.mood} stress={self.stress} "
            f"({self.created_at:%Y-%m-%d})"
        )