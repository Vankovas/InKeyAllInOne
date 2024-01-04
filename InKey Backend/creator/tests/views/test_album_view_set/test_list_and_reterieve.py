from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album


class TestRetrieveAndListAlbumView(TestUserMixin):
    def setUp(self) -> None:
        super(TestRetrieveAndListAlbumView, self).setUp()
        self.albums = [
            Album.objects.create(name="yes1", artist=self.user),
            Album.objects.create(name="yes2", artist=self.user),
            Album.objects.create(
                name="yes3", artist=self.user, description="yes33333333", views=10
            )
        ]
        self.albums[2].cover_image = self.get_image_for_upload()
        self.albums[2].save()

        self.albums_other = [
            Album.objects.create(name="no1", artist=self.user_other),
            Album.objects.create(name="no2", artist=self.user_other),
            Album.objects.create(name="nope3", artist=self.user_other, is_private=True),
        ]
    
    def test_list_albums_unauthenticated(self):
        response = self.client_unauthenticated.get(reverse("album-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
    def test_retrieve_album_unauthenticated(self):
        response = self.client_unauthenticated.get(reverse("album-detail", kwargs={"pk": self.albums[0].pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_list_albums_works(self):
        response = self.client.get(reverse("album-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        all_albums = response.json()
        self.assertEqual(len(all_albums), 5)

    def test_retrieve_album_works_and_icreases_views_count(self):
        response = self.client.get(reverse("album-detail", kwargs={"pk": self.albums[2].pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        album = response.json()
        self.assertEqual(album["name"], self.albums[2].name)
        self.assertEqual(album["description"], self.albums[2].description)
        self.assertEqual(album["views"], self.albums[2].views + 1)
        self.albums[2].refresh_from_db()
        self.assertEqual(album["views"], self.albums[2].views)
        self.assertEqual(album["is_private"], self.albums[2].is_private)

    def test_retrieve_private_album_works_if_album_belongs_to_user(self):
        response = self.client_other.get(reverse("album-detail", kwargs={"pk": self.albums_other[2].pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        album = response.json()
        self.assertEqual(album["name"], self.albums_other[2].name)

    def test_retrieve_private_album_doesnt_work_if_album_doesnt_belong_to_user(self):
        response = self.client.get(reverse("album-detail", kwargs={"pk": self.albums_other[2].pk}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_retreve_album_returns_artist_name(self):
        self.user.firstname = "This is my name"
        self.user.save()
        response = self.client.get(reverse("album-detail", kwargs={"pk": self.albums[2].pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        album = response.json()
        self.assertEqual(album["artist_name"], "This is my name")
        self.assertEqual(album["artist_name"], self.user.firstname)
