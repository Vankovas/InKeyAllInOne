from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album


class TestUpdateAlbumView(TestUserMixin):
    def setUp(self) -> None:
        super(TestUpdateAlbumView, self).setUp()
        self.album = Album.objects.create(name="yes", artist=self.user)
        self.album_other = Album.objects.create(name="no", artist=self.user_other)

    def test_update_album_unauthenticated(self):
        response = self.client_unauthenticated.put(
            reverse("album-detail", kwargs={"pk": self.album.pk}),
            {
                "name": "newer name",
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.album.refresh_from_db()
        self.assertNotEqual(self.album.name, "newer name")

    def test_update_album_works(self):
        response = self.client.put(
            reverse("album-detail", kwargs={"pk": self.album.pk}),
            {
                "name": "newer name"
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.album.refresh_from_db()
        self.assertEqual(self.album.name, "newer name")

    def test_update_album_of_another_person_raises_error(self):
        response = self.client.put(
            reverse("album-detail", kwargs={"pk": self.album_other.pk}),
            {
                "name": "newer name",
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.album_other.refresh_from_db()
        self.assertNotEqual(self.album_other.name, "newer name")
