from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album


class TestDeleteAlbumView(TestUserMixin):
    def setUp(self) -> None:
        super(TestDeleteAlbumView, self).setUp()
        self.album = Album.objects.create(name="yes", artist=self.user)
        self.album_other = Album.objects.create(name="no", artist=self.user_other)

    def test_delete_album_unauthenticated(self):
        response = self.client_unauthenticated.delete(
            reverse("album-detail", kwargs={"pk": self.album.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(Album.objects.filter(artist=self.user).count(), 1)

    def test_delete_album_works(self):
        response = self.client.delete(
            reverse("album-detail", kwargs={"pk": self.album.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Album.objects.filter(artist=self.user).count(), 0)

    def test_delete_album_of_another_person_raises_error(self):
        response = self.client.delete(
            reverse("album-detail", kwargs={"pk": self.album_other.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Album.objects.filter(artist=self.user_other).count(), 1)
