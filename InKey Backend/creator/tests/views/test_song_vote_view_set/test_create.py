from django.urls import reverse

from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import SongVote, Song, Album


class TestCreateSongVoteViewset(TestUserMixin):
    def setUp(self) -> None:
        super(TestCreateSongVoteViewset, self).setUp()
        self.album = Album.objects.create(name="yes1", artist=self.user)
        self.songs = [
            Song.objects.create(name="name1", album=self.album),
            Song.objects.create(name="name2", album=self.album),
        ]

    def test_create_works_properly(self):
        self.assertEqual(SongVote.objects.count(), 0)
        response = self.client.post(reverse("song_vote-list"), data={"song": self.songs[0].id, "rating": 3})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SongVote.objects.count(), 1)
        self.assertEqual(SongVote.objects.get().user_id, self.user.id)
        self.assertEqual(SongVote.objects.get().song_id, self.songs[0].id)
        self.assertEqual(SongVote.objects.get().rating, 3)

    def test_create_from_another_user_works_properly(self):
        response = self.client_other.post(reverse("song_vote-list"), data={"song": self.songs[0].id, "rating": 3})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SongVote.objects.count(), 1)
        self.assertEqual(SongVote.objects.get().user_id, self.user_other.id)
        self.assertEqual(SongVote.objects.get().song_id, self.songs[0].id)
        self.assertEqual(SongVote.objects.get().rating, 3)

    def test_unauthenticated_not_allowed(self):
        response = self.client_unauthenticated.post(reverse("song_vote-list"),
                                                    data={"song": self.songs[0].id, "rating": 3})
        self.assertEqual(response.status_code, 401)

    def test_song_rating_is_average_of_all_song_votes(self):
        response = self.client_other.post(reverse("song_vote-list"), data={"song": self.songs[0].id, "rating": 0})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse("song_vote-list"), data={"song": self.songs[0].id, "rating": 5})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.songs[0].rating_calculated, 2.5)

    def test_user_updates_his_rating_when_tries_to_create_for_a_second_time(self):
        self.assertEqual(SongVote.objects.count(), 0)
        response = self.client.post(reverse("song_vote-list"), data={"song": self.songs[0].id, "rating": 3})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.songs[0].rating_calculated, 3)
        self.assertEqual(SongVote.objects.count(), 1)
        vote_id = SongVote.objects.get().id
        response = self.client.post(reverse("song_vote-list"), data={"song": self.songs[0].id, "rating": 1})
        self.assertEqual(response.status_code, 201)
        self.songs[0].refresh_from_db()
        self.assertEqual(SongVote.objects.count(), 1)
        self.assertEqual(SongVote.objects.get().id, vote_id)
        self.assertEqual(self.songs[0].rating_calculated, 1)
