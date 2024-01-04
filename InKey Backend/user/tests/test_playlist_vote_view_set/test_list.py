from django.urls import reverse

from account_management.tests.mixin.test_user_mixin import TestUserMixin
from user.models import PlaylistVote, Playlist


class TestListPlaylistVoteViewset(TestUserMixin):
    def setUp(self) -> None:
        super(TestListPlaylistVoteViewset, self).setUp()
        self.playlists = [
            Playlist.objects.create(name="yes1", user=self.user),
            Playlist.objects.create(name="yes2", user=self.user),
            Playlist.objects.create(
                name="yes3", user=self.user, description="yes33333333", views=10
            )
        ]
        PlaylistVote.objects.create(user=self.user, playlist=self.playlists[0], rating=5)
        PlaylistVote.objects.create(user=self.user, playlist=self.playlists[1], rating=2)
        PlaylistVote.objects.create(user=self.user_other, playlist=self.playlists[1], rating=3)

    def test_list_works_properly(self):
        response = self.client.get(reverse("playlist_vote-list"))
        rjson = response.json()
        self.assertEqual(len(rjson), 2)
        for vote in rjson:
            if vote["playlist"] == self.playlists[0].id:
                self.assertEqual(vote["rating"], 5)
            elif vote["playlist"] == self.playlists[1].id:
                self.assertEqual(vote["rating"], 2)
            else:
                self.fail("You have a vote with incorrect playlist id")
        response = self.client_other.get(reverse("playlist_vote-list"))
        self.assertEqual(response.status_code, 200)
        rjson = response.json()
        self.assertEqual(len(rjson), 1)
        self.assertEqual(rjson[0]["rating"], 3)

    def test_list_filter_by_playlist_id(self):
        response = self.client.get(reverse("playlist_vote-list")+f"?playlist__id={self.playlists[0].id}")
        rjson = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(rjson), 1)
        self.assertEqual(rjson[0]["rating"], 5)

    def test_unauthenticated_not_allowed(self):
        response = self.client_unauthenticated.get(reverse("playlist_vote-list"))
        self.assertEqual(response.status_code, 401)

    def test_playlist_rating_is_average_of_all_playlist_votes(self):
        response = self.client_unauthenticated.get(reverse("playlist-detail", kwargs={"pk": self.playlists[1].pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["rating"], 2.5)
