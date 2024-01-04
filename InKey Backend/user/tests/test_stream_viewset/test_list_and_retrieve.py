import uuid
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from user.models import Stream


class TestGetStream(TestUserMixin):
    def setUp(self) -> None:
        super(TestGetStream, self).setUp()
        self.streams = [
            self.create_streamer_and_stream(self.user),
            self.create_streamer_and_stream(self.user_other),
            self.create_streamer_and_stream(),
            self.create_streamer_and_stream(),
            self.create_streamer_and_stream(),
        ]

    def create_streamer_and_stream(self, artist=None):
        if not artist:
            artist = self.create_user(str(uuid.uuid4())+"@email.com", str(uuid.uuid4()))
        return Stream.objects.create(artist=artist)

    def test_get_streams_gets_the_streams(self):
        response = self.client.get(reverse("stream-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Stream.objects.count(), len(response.json()))

    def test_get_streams_unauthenticated_still_works(self):
        response = self.client_unauthenticated.get(reverse("stream-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Stream.objects.count(), len(response.json()))

    def test_get_stream_gets_the_correct_stream(self):
        response = self.client.get(reverse("stream-detail", kwargs={"artist__id": self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], str(Stream.objects.get(artist=self.user).uuid))
        self.assertTrue("artist" in response.json())

    def test_get_stream_unauthenticated_still_works(self):
        response = self.client_unauthenticated.get(reverse("stream-detail", kwargs={"artist__id": self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], str(Stream.objects.get(artist=self.user).uuid))
        self.assertTrue("artist" in response.json())
        print(response.json())

    def test_get_stream_with_non_existing_user_id_gives_404_error(self):
        response = self.client.get(reverse("stream-detail", kwargs={"artist__id": -1}))
        self.assertEqual(response.status_code, 404)
