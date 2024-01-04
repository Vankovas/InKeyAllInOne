from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from user.models import FavoriteArtist


class TestListFavoriteArtistViewSet(TestUserMixin):
    def setUp(self) -> None:
        super(TestListFavoriteArtistViewSet, self).setUp()
        self.artist = [
            self.create_user(email="email1@emial.com", password="123"),
            self.create_user(email="email2@emial.com", password="456"),
            self.create_user(email="email3@emial.com", password="789")
        ]
        self.favorite_artist = [
            FavoriteArtist.objects.create(user_id=self.user.id, artist_id=self.artist[0].id),
            FavoriteArtist.objects.create(user_id=self.user.id, artist_id=self.artist[2].id)
        ]

    def test_list_favorite_artists_unauthenticated(self):
        response = self.client_unauthenticated.get(reverse("favorite_artist-list"))
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_favorite_artists_works(self):
        response = self.client.get(reverse("favorite_artist-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        all_artists = response.json()
        self.assertEqual(len(all_artists), 2)
