import json 

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..models import Moods, TrackPlayed, BookMarkedSong
from django.urls import reverse


User = get_user_model()

class TrackPlayedModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )

    def test_track_creation(self):
        track = TrackPlayed.objects.create(
            user=self.user,
            track_id="123",
            track_name="Song A",
            artist_name="Artist A",
            album_name="Album A",
            image_url="http://example.com/img.jpg",
            audio_url="http://example.com/audio.mp3",
            duration=120.0
        )

        self.assertEqual(track.track_id, "123")
        self.assertEqual(track.user.username, "testuser")

class TrackPlayedAPITest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )
        self.client.login(username="testuser", password="12345")

    def test_track_played_post(self):
        data = {
            "track_id": "123",
            "track_name": "Song A",
            "artist_name": "Artist A",
            "album_name": "Album A",
            "image_url": "http://example.com/img.jpg",
            "audio_url": "http://example.com/audio.mp3",
            "duration": 120
        }

        response = self.client.post(
            reverse("home:track_played"),
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(TrackPlayed.objects.count(), 1)