from django.urls import reverse

from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album, Song
from user.models import Comment, CommentSong


class TestCreateCommentOnSong(TestUserMixin):
    def setUp(self) -> None:
        super(TestCreateCommentOnSong, self).setUp()
        self.album = Album.objects.create(name="yes1", artist=self.user)
        self.album_other = Album.objects.create(name="yes2", artist=self.user_other)
        self.song = Song.objects.create(name="song1", album=self.album)
        self.song_other = Song.objects.create(name="song_other1", album=self.album_other)
        self.make_comment(self.user, self.song, "Another message 0")
        self.make_comment(self.user, self.song, "Another message 1")
        self.make_comment(self.user_other, self.song, "Another message 2")
        self.make_comment(self.user_other, self.song_other, "Another message 3")
        self.make_comment(self.user, self.song_other, "Another message 4")

    def make_comment(self, user, song, message="Random message!"):
        c = Comment.objects.create(message=message, user=user)
        return CommentSong.objects.create(song=song, comment=c)

    def test_get_all_song_comments(self):
        response = self.client.get(reverse('comment_song-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)
        for (index, cs) in enumerate(response.json()):
            real_comment = Comment.objects.get(id=cs["comment"]["id"])
            self.assertEqual(cs["comment"]["message"], real_comment.message)
            self.assertEqual(cs["comment"]["user"], real_comment.user.id)
            if index<3:
                self.assertEqual(cs["song_id"], self.song.id)
            else:
                self.assertEqual(cs["song_id"], self.song_other.id)

    def test_get_all_song_comments_of_specific_song(self):
        response = self.client.get(reverse('comment_song-list')+f"?song={self.song.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        for cs in response.json():
            self.assertEqual(cs["song_id"], self.song.id)
        response = self.client.get(reverse('comment_song-list') + f"?song={self.song_other.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        for cs in response.json():
            self.assertEqual(cs["song_id"], self.song_other.id)

    def test_unauthenticated_user_can_view_coments(self):
        response = self.client_unauthenticated.get(reverse('comment_song-list'))
        self.assertEqual(response.status_code, 200)