from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import MoodEntry
import random


class Command(BaseCommand):
    help = "Generate test data"

    def handle(self, *args, **kwargs):

        # napravi test usera
        user, created = User.objects.get_or_create(
            username="testuser"
        )

        if created:
            user.set_password("test1234")
            user.save()

        # napravi mood unose
        for i in range(20):
            MoodEntry.objects.create(
                user=user,
                mood=random.randint(1, 10),
                stress=random.randint(1, 10),
                note=f"Test note {i}"
            )

        self.stdout.write(self.style.SUCCESS("Test data generated!"))