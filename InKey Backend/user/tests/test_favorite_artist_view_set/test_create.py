from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from user.models import FavoriteArtist


class TestCreateFavoriteArtistViewSet(TestUserMixin):
    def setUp(self) -> None:
        super(TestCreateFavoriteArtistViewSet, self).setUp()

    def test_add_to_favorite_works(self):
        data = {
            'artist_id': self.user_other.id
        }
        response = self.client.post(reverse("favorite_artist-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_add_to_favorite_twice_delete(self):
        data = {
            'artist_id': self.user_other.id
        }
        self.client.post(reverse("favorite_artist-list"), data)
        print(f'Artist is added to database: {FavoriteArtist.objects.all()}')
        response = self.client.post(reverse("favorite_artist-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        print(f'Artist is removed from database: {FavoriteArtist.objects.all()}')

    def test_add_to_favorite_no_such_artist(self):
        data = {
            'artist_id': -1
        }
        response = self.client.post(reverse("favorite_artist-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()["user"], "User does not exist")

    def test_add_favorite_artist_unauthenticated(self):
        data = {
            'artist_id': self.user_other.id
        }
        response = self.client_unauthenticated.post(reverse("favorite_artist-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_add_favorite_artist_yourself(self):
        data = {
            'artist_id': self.user.id
        }
        response = self.client.post(reverse("favorite_artist-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()["user"], "You cannot like yourself.")
