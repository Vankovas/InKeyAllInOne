from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from user.models import Stream


class TestCreateStream(TestUserMixin):
    def test_create_stream_creates_the_stream(self):
        response = self.client.post(reverse("stream-list"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Stream.objects.count(), 1)
        self.assertEqual(Stream.objects.get().artist, self.user)

    def test_create_stream_unauthenticated_doesnt_do_anything(self):
        response = self.client_unauthenticated.post(reverse("stream-list"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Stream.objects.count(), 0)

    def test_create_stream_secondtime_doesnt_create_duplicate_but_returns_stream(self):
        Stream.objects.create(artist=self.user)
        response = self.client.post(reverse("stream-list"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Stream.objects.count(), 1)
