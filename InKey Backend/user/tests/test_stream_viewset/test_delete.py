import uuid
from django.urls import reverse

from account_management.tests.mixin.test_user_mixin import TestUserMixin
from user.models import Stream


class TestDeleteStream(TestUserMixin):
    def setUp(self) -> None:
        super(TestDeleteStream, self).setUp()
        self.streams = [
            self.create_streamer_and_stream(self.user),
            self.create_streamer_and_stream(self.user_other),
        ]

    def create_streamer_and_stream(self, artist=None):
        if not artist:
            artist = self.create_user(str(uuid.uuid4())+"@email.com", str(uuid.uuid4()))
        return Stream.objects.create(artist=artist)

    def test_delete_stream_deletes_the_stream(self):
        self.assertEqual(Stream.objects.filter(artist=self.user).count(), 1)
        response = self.client.delete(reverse("stream-detail", kwargs={"artist__id": self.user.id}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Stream.objects.filter(artist=self.user).count(), 0)

    def test_delete_stream_of_other_does_not_delete_the_stream(self):
        self.assertEqual(Stream.objects.filter(artist=self.user).count(), 1)
        response = self.client_other.delete(reverse("stream-detail", kwargs={"artist__id": self.user.id}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Stream.objects.filter(artist=self.user).count(), 1)

    def test_unauthenticated_user_does_not_delete_the_stream(self):
        self.assertEqual(Stream.objects.filter(artist=self.user).count(), 1)
        response = self.client_unauthenticated.delete(reverse("stream-detail", kwargs={"artist__id": self.user.id}))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Stream.objects.filter(artist=self.user).count(), 1)

    def test_deleting_non_existing_stream_gives_404(self):
        response = self.client.delete(reverse("stream-detail", kwargs={"artist__id": self.user.id}))
        self.assertEqual(response.status_code, 204)
        response = self.client.delete(reverse("stream-detail", kwargs={"artist__id": self.user.id}))
        self.assertEqual(response.status_code, 404)
