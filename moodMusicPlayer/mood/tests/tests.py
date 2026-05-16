from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Moods, TrackPlayed, BookMarkedSong

class MoodModelTest(TestCase):

    def test_mood_creation(self):
        mood = Moods.objects.create(
            name="Happy Mood",
            type="HA"
        )

        self.assertEqual(mood.name, "Happy Mood")
        self.assertEqual(mood.type, "HA")

    

    