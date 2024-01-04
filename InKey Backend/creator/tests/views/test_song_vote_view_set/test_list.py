from django.urls import reverse

from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import SongVote, Album, Song


class TestListSongVoteViewset(TestUserMixin):
    def setUp(self) -> None:
        super(TestListSongVoteViewset, self).setUp()
        self.album = Album.objects.create(name="yes1", artist=self.user)
        self.songs = [
            Song.objects.create(name="name1", album=self.album),
            Song.objects.create(name="name2", album=self.album),
        ]
        SongVote.objects.create(user=self.user, song=self.songs[0], rating=5)
        SongVote.objects.create(user=self.user, song=self.songs[1], rating=2)
        SongVote.objects.create(user=self.user_other, song=self.songs[1], rating=3)

    def test_list_works_properly(self):
        response = self.client.get(reverse("song_vote-list"))
        rjson = response.json()
        self.assertEqual(len(rjson), 2)
        for vote in rjson:
            if vote["song"] == self.songs[0].id:
                self.assertEqual(vote["rating"], 5)
            elif vote["song"] == self.songs[1].id:
                self.assertEqual(vote["rating"], 2)
            else:
                self.fail("You have a vote with incorrect song id")
        response = self.client_other.get(reverse("song_vote-list"))
        self.assertEqual(response.status_code, 200)
        rjson = response.json()
        self.assertEqual(len(rjson), 1)
        self.assertEqual(rjson[0]["rating"], 3)

    def test_list_filter_by_song_id(self):
        response = self.client.get(reverse("song_vote-list")+f"?song__id={self.songs[0].id}")
        rjson = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(rjson), 1)
        self.assertEqual(rjson[0]["rating"], 5)

    def test_unauthenticated_not_allowed(self):
        response = self.client_unauthenticated.get(reverse("song_vote-list"))
        self.assertEqual(response.status_code, 401)

    def test_song_rating_is_average_of_all_song_votes(self):
        response = self.client_unauthenticated.get(reverse("song-detail", kwargs={"pk": self.songs[1].pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["rating"], 2.5)
