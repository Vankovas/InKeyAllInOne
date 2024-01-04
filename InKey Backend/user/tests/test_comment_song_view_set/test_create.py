from django.urls import reverse

from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album, Song
from user.models import CommentSong, Comment


class TestCreateCommentOnSong(TestUserMixin):
    def setUp(self) -> None:
        super(TestCreateCommentOnSong, self).setUp()
        album = Album.objects.create(name="yes1", artist=self.user)
        album_other = Album.objects.create(name="yes2", artist=self.user_other)
        self.full_object = {
            "name": "name1",
            "album": album,
            "views": 100,
            "description": "Yes",
            "data": self.get_wav_audio_for_upload()
        }
        self.song = Song.objects.create(**self.full_object)
        self.song_other = Song.objects.create(name="other1", album=album_other)
        self.creation_data = {
            'comment': {
                "message": "hey you sux"
            },
            "song_id": self.song.id
        }

    def assert_create_is_correct(self, response, song, user):
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CommentSong.objects.count(), 1)
        self.assertEqual(CommentSong.objects.get().comment, Comment.objects.get())
        self.assertEqual(CommentSong.objects.get().song, song)
        self.assertEqual(CommentSong.objects.get().comment.user.id, user.id)

    def test_create_comment_works(self):
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CommentSong.objects.count(), 0)
        response = self.client.post(reverse('comment_song-list'), data=self.creation_data, format='json')
        self.assert_create_is_correct(response, self.song, self.user)

    def test_create_comment_on_another_persons_song_works(self):
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CommentSong.objects.count(), 0)
        self.creation_data["song_id"] = self.song_other.id
        response = self.client.post(reverse('comment_song-list'), data=self.creation_data, format='json')
        self.assert_create_is_correct(response, self.song_other, self.user)

    def test_create_comment_not_logged_in_doesnt_work(self):
        response = self.client_unauthenticated.post(
            reverse('comment_song-list'),
            data=self.creation_data,
            format='json'
        )
        self.assertEqual(response.status_code, 401)

    def test_create_comment_with_non_existing_song_doesnt_work(self):
        self.creation_data["song_id"] = -1
        response = self.client.post(
            reverse('comment_song-list'),
            data=self.creation_data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()[0], 'Enter a correct song id!!!')

    def test_create_comment_twice_works(self):
        response = self.client.post(reverse('comment_song-list'), data=self.creation_data, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse('comment_song-list'), data=self.creation_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(CommentSong.objects.count(), 2)
        for cs in CommentSong.objects.all():
            self.assertEqual(cs.song, self.song)
            self.assertEqual(cs.comment.user.id, self.user.id)
