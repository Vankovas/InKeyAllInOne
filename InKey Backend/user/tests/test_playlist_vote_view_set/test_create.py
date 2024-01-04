from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from user.models import PlaylistVote, Playlist


class TestCreatePlaylistVoteViewset(TestUserMixin):
    def setUp(self) -> None:
        super(TestCreatePlaylistVoteViewset, self).setUp()
        self.playlists = [
            Playlist.objects.create(name="yes1", user=self.user),
            Playlist.objects.create(name="yes2", user=self.user),
            Playlist.objects.create(
                name="yes3", user=self.user, description="yes33333333", views=10
            )
        ]

    def test_create_works_properly(self):
        self.assertEqual(PlaylistVote.objects.count(), 0)
        response = self.client.post(reverse("playlist_vote-list"), data={"playlist": self.playlists[0].id, "rating": 3})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PlaylistVote.objects.count(), 1)
        self.assertEqual(PlaylistVote.objects.get().user_id, self.user.id)
        self.assertEqual(PlaylistVote.objects.get().playlist_id, self.playlists[0].id)
        self.assertEqual(PlaylistVote.objects.get().rating, 3)

    def test_create_from_another_user_works_properly(self):
        response = self.client_other.post(reverse("playlist_vote-list"), data={"playlist": self.playlists[0].id, "rating": 3})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PlaylistVote.objects.count(), 1)
        self.assertEqual(PlaylistVote.objects.get().user_id, self.user_other.id)
        self.assertEqual(PlaylistVote.objects.get().playlist_id, self.playlists[0].id)
        self.assertEqual(PlaylistVote.objects.get().rating, 3)

    def test_unauthenticated_not_allowed(self):
        response = self.client_unauthenticated.post(reverse("playlist_vote-list"),
                                                    data={"playlist": self.playlists[0].id, "rating": 3})
        self.assertEqual(response.status_code, 401)

    def test_playlist_rating_is_average_of_all_playlist_votes(self):
        response = self.client_other.post(reverse("playlist_vote-list"), data={"playlist": self.playlists[0].id, "rating": 0})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse("playlist_vote-list"), data={"playlist": self.playlists[0].id, "rating": 5})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.playlists[0].rating_calculated, 2.5)

    def test_user_updates_his_rating_when_tries_to_create_for_a_second_time(self):
        self.assertEqual(PlaylistVote.objects.count(), 0)
        response = self.client.post(reverse("playlist_vote-list"), data={"playlist": self.playlists[0].id, "rating": 5})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.playlists[0].rating_calculated, 5)
        self.assertEqual(PlaylistVote.objects.count(), 1)
        vote_id = PlaylistVote.objects.get().id
        response = self.client.post(reverse("playlist_vote-list"), data={"playlist": self.playlists[0].id, "rating": 2})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.playlists[0].rating_calculated, 2)
        self.assertEqual(PlaylistVote.objects.count(), 1)
        self.assertEqual(PlaylistVote.objects.get().id, vote_id)
