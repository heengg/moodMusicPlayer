from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Moods, TrackPlayed, BookMarkedSong
from ..forms import MoodsForm

class MoodFormTest(TestCase):

    def test_valid_form(self):
        form = MoodsForm(data={
            "type": "HA"
        })

        self.assertTrue(form.is_valid())