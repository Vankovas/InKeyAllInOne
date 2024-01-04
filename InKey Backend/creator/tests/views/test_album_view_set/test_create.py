from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin


class TestCreateAlbumView(TestUserMixin):
    def test_create_album(self):
        response = self.client.post(reverse("album-list"), {"name": "new album"})
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response_json = response.json()
        self.assertEqual(response_json["name"], "new album")
        self.assertNotEqual(response_json["artist"], self.user_other.pk)
        self.assertEqual(response_json["artist"], self.user.pk)

    def test_create_album_without_name_raises_error(self):
        response = self.client.post(reverse("song-list"), {"artist": self.user.pk})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_album_without_artist_raises_error(self):
        response = self.client.post(reverse("song-list"), {"name": "haha"})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_album_unauthenticated(self):
        response = self.client_unauthenticated.post(reverse("album-list"), {"name": "new album"})
        print(response.json())
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_create_album_with_other_user_id_still_creates_it_to_you(self):
        response = self.client.post(reverse("album-list"), {"name": "new album", "artist": self.user_other.pk})
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response_json = response.json()
        self.assertEqual(response_json["name"], "new album")
        self.assertEqual(response_json["artist"], self.user.pk)

    def test_create_album_with_views_doesnt_init_the_views(self):
        response = self.client.post(reverse("album-list"), {"name": "new album", "views": 100})
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response_json = response.json()
        self.assertEqual(response_json["views"], 0)

    def test_create_album_with_all_fields(self):
        album_body = {
            "name": "newer name",
            "description": "newer description",
            "cover_image": self.get_image_for_upload(),
            "views": 100,
            "is_private": True,
            "artist": -1,
        }
        response = self.client.post(reverse("album-list"), album_body)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response_json = response.json()
        self.assertEqual(response_json["name"], album_body["name"])
        self.assertEqual(response_json["description"], album_body["description"])
        self.assertIn(album_body["cover_image"].name[:-4], response_json["cover_image"])
        self.assertEqual(response_json["is_private"], True)
        self.assertNotEqual(response_json["artist"], self.user_other.pk)
        self.assertNotEqual(response_json["views"], album_body["views"])
        self.assertEqual(response_json["views"], 0)
        self.assertEqual(response_json["artist"], self.user.pk)
        self.assertNotEqual(response_json["artist"], album_body["artist"])
