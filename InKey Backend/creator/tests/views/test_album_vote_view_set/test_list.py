from django.urls import reverse

from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import AlbumVote, Album


class TestListAlbumVoteViewset(TestUserMixin):
    def setUp(self) -> None:
        super(TestListAlbumVoteViewset, self).setUp()
        self.albums = [
            Album.objects.create(name="yes1", artist=self.user),
            Album.objects.create(name="yes2", artist=self.user),
            Album.objects.create(
                name="yes3", artist=self.user, description="yes33333333", views=10
            )
        ]
        AlbumVote.objects.create(user=self.user, album=self.albums[0], rating=5)
        AlbumVote.objects.create(user=self.user, album=self.albums[1], rating=2)
        AlbumVote.objects.create(user=self.user_other, album=self.albums[1], rating=3)

    def test_list_works_properly(self):
        response = self.client.get(reverse("album_vote-list"))
        rjson = response.json()
        self.assertEqual(len(rjson), 2)
        for vote in rjson:
            if vote["album"] == self.albums[0].id:
                self.assertEqual(vote["rating"], 5)
            elif vote["album"] == self.albums[1].id:
                self.assertEqual(vote["rating"], 2)
            else:
                self.fail("You have a vote with incorrect album id")
        response = self.client_other.get(reverse("album_vote-list"))
        self.assertEqual(response.status_code, 200)
        rjson = response.json()
        self.assertEqual(len(rjson), 1)
        self.assertEqual(rjson[0]["rating"], 3)

    def test_list_filter_by_album_id(self):
        response = self.client.get(reverse("album_vote-list")+f"?album__id={self.albums[0].id}")
        rjson = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(rjson), 1)
        self.assertEqual(rjson[0]["rating"], 5)

    def test_unauthenticated_not_allowed(self):
        response = self.client_unauthenticated.get(reverse("album_vote-list"))
        self.assertEqual(response.status_code, 401)

    def test_album_rating_is_average_of_all_album_votes(self):
        response = self.client_unauthenticated.get(reverse("album-detail", kwargs={"pk": self.albums[1].pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["rating"], 2.5)
