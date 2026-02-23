from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import MoodEntry, MeditationSession, Tag


class MainAppTests(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(username="user1", password="pass12345")
        self.other_user = User.objects.create_user(username="user2", password="pass12345")

        self.tag1 = Tag.objects.create(name="stres")
        self.tag2 = Tag.objects.create(name="sreća")

        self.mood1 = MoodEntry.objects.create(
            user=self.user,
            mood=7,
            stress=4,
            note="Danas sam OK",
        )
        self.mood1.tags.set([self.tag1])

        self.mood2 = MoodEntry.objects.create(
            user=self.user,
            mood=3,
            stress=9,
            note="Puno anksioznosti",
        )
        self.mood2.tags.set([self.tag2])

        self.med1 = MeditationSession.objects.create(user=self.user, duration_minutes=10)
        self.med_other = MeditationSession.objects.create(user=self.other_user, duration_minutes=20)


    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse("dashboard"))
        self.assertEqual(resp.status_code, 302)

    def test_mood_list_requires_login(self):
        resp = self.client.get(reverse("mood_list"))
        self.assertEqual(resp.status_code, 302)

    def test_meditation_list_requires_login(self):
        resp = self.client.get(reverse("meditation_list"))
        self.assertEqual(resp.status_code, 302)


    def test_create_mood_assigns_user(self):
        self.client.force_login(self.user)

        resp = self.client.post(
            reverse("mood_create"),
            data={
                "mood": 8,
                "stress": 2,
                "note": "Test unos",
                "tags": [self.tag1.id, self.tag2.id],
            },
        )
        self.assertEqual(resp.status_code, 302)
        created = MoodEntry.objects.filter(user=self.user, note="Test unos").first()
        self.assertIsNotNone(created)
        self.assertEqual(created.mood, 8)
        self.assertEqual(created.stress, 2)
        self.assertEqual(set(created.tags.all()), {self.tag1, self.tag2})

    def test_mood_search_by_note(self):
        self.client.force_login(self.user)

        resp = self.client.get(reverse("mood_list"), {"q": "anksioznosti"})
        self.assertEqual(resp.status_code, 200)

        moods = list(resp.context["moods"])
        self.assertIn(self.mood2, moods)
        self.assertNotIn(self.mood1, moods)

    def test_mood_search_by_tag(self):
        self.client.force_login(self.user)

        resp = self.client.get(reverse("mood_list"), {"q": "stres"})
        self.assertEqual(resp.status_code, 200)

        moods = list(resp.context["moods"])
        self.assertIn(self.mood1, moods)
        self.assertNotIn(self.mood2, moods)

    def test_user_cannot_edit_other_users_mood(self):
        self.client.force_login(self.other_user)

        resp = self.client.post(
            reverse("mood_edit", args=[self.mood1.pk]),
            data={"mood": 1, "stress": 1, "note": "Hacked", "tags": []},
        )
        self.assertEqual(resp.status_code, 404)


    def test_meditation_list_shows_only_own_sessions(self):
        self.client.force_login(self.user)

        resp = self.client.get(reverse("meditation_list"))
        self.assertEqual(resp.status_code, 200)

        sessions = list(resp.context["sessions"])
        self.assertIn(self.med1, sessions)
        self.assertNotIn(self.med_other, sessions)

    def test_delete_meditation_is_post_only(self):
        self.client.force_login(self.user)

        resp = self.client.get(reverse("meditation_delete", args=[self.med1.pk]))
        self.assertEqual(resp.status_code, 405)

    def test_user_can_delete_own_meditation(self):
        self.client.force_login(self.user)

        resp = self.client.post(reverse("meditation_delete", args=[self.med1.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(MeditationSession.objects.filter(pk=self.med1.pk).exists())

    def test_user_cannot_delete_other_users_meditation(self):
        self.client.force_login(self.user)

        resp = self.client.post(reverse("meditation_delete", args=[self.med_other.pk]))
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(MeditationSession.objects.filter(pk=self.med_other.pk).exists())