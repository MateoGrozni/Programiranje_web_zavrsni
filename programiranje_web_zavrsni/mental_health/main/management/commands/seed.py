from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from main.models import MoodEntry, MeditationSession, Tag
import random


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
        )

    def handle(self, *args, **options):
        User = get_user_model()

        if options["clear"]:
            MoodEntry.objects.all().delete()
            MeditationSession.objects.all().delete()

        user, created = User.objects.get_or_create(username="testuser")
        if created:
            user.set_password("test1234")
            user.save()

        tags = list(Tag.objects.all())

        for i in range(20):
            mood = MoodEntry.objects.create(
                user=user,
                mood=random.randint(1, 10),
                stress=random.randint(1, 10),
                note=f"Test note {i}",
            )

            if tags:
                chosen = random.sample(tags, k=random.randint(0, min(3, len(tags))))
                mood.tags.set(chosen)

        for _ in range(15):
            MeditationSession.objects.create(
                user=user,
                duration_minutes=random.choice([5, 10, 12, 15, 20, 25, 30]),
            )

        self.stdout.write(self.style.SUCCESS("Test data generated!"))