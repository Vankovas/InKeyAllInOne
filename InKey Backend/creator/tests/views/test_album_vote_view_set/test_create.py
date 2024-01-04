from django.urls import reverse

from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import AlbumVote, Album


class TestCreateAlbumVoteViewset(TestUserMixin):
    def setUp(self) -> None:
        super(TestCreateAlbumVoteViewset, self).setUp()
        self.albums = [
            Album.objects.create(name="yes1", artist=self.user),
            Album.objects.create(name="yes2", artist=self.user),
            Album.objects.create(
                name="yes3", artist=self.user, description="yes33333333", views=10
            )
        ]

    def test_create_works_properly(self):
        self.assertEqual(AlbumVote.objects.count(), 0)
        response = self.client.post(reverse("album_vote-list"), data={"album": self.albums[0].id, "rating": 3})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AlbumVote.objects.count(), 1)
        self.assertEqual(AlbumVote.objects.get().user_id, self.user.id)
        self.assertEqual(AlbumVote.objects.get().album_id, self.albums[0].id)
        self.assertEqual(AlbumVote.objects.get().rating, 3)

    def test_create_from_another_user_works_properly(self):
        response = self.client_other.post(reverse("album_vote-list"), data={"album": self.albums[0].id, "rating": 3})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AlbumVote.objects.count(), 1)
        self.assertEqual(AlbumVote.objects.get().user_id, self.user_other.id)
        self.assertEqual(AlbumVote.objects.get().album_id, self.albums[0].id)
        self.assertEqual(AlbumVote.objects.get().rating, 3)

    def test_unauthenticated_not_allowed(self):
        response = self.client_unauthenticated.post(reverse("album_vote-list"),
                                                    data={"album": self.albums[0].id, "rating": 3})
        self.assertEqual(response.status_code, 401)

    def test_album_rating_is_average_of_all_album_votes(self):
        response = self.client_other.post(reverse("album_vote-list"), data={"album": self.albums[0].id, "rating": 0})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse("album_vote-list"), data={"album": self.albums[0].id, "rating": 5})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.albums[0].rating_calculated, 2.5)

    def test_user_updates_his_rating_when_tries_to_create_for_a_second_time(self):
        self.assertEqual(AlbumVote.objects.count(), 0)
        response = self.client.post(reverse("album_vote-list"), data={"album": self.albums[0].id, "rating": 5})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.albums[0].rating_calculated, 5)
        self.assertEqual(AlbumVote.objects.count(), 1)
        vote_id = AlbumVote.objects.get().id
        response = self.client.post(reverse("album_vote-list"), data={"album": self.albums[0].id, "rating": 2})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.albums[0].rating_calculated, 2)
        self.assertEqual(AlbumVote.objects.count(), 1)
        self.assertEqual(AlbumVote.objects.get().id, vote_id)
