from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album
from user.models import Comment, CommentAlbum


class TestCreateCommentOnAlbum(TestUserMixin):
    def setUp(self) -> None:
        super(TestCreateCommentOnAlbum, self).setUp()
        self.album = Album.objects.create(name="yes1", artist=self.user)
        self.album_private = Album.objects.create(name="yes2", artist=self.user, is_private=True)
        self.album_other = Album.objects.create(name="yes3", artist=self.user_other)
        self.make_comment(self.user,  self.album, "Another message 0")
        self.make_comment(self.user,  self.album_private, "Another message 1")
        self.make_comment(self.user_other, self.album_other, "Another message 2")

    def make_comment(self, user, album, message="Random message!"):
        c = Comment.objects.create(message=message, user=user)
        return CommentAlbum.objects.create(album=album, comment=c)

    def test_get_all_album_comments(self):
        response = self.client.get(reverse('comment_album-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        print(response.json())
        for (index, cs) in enumerate(response.json()):
            real_comment = Comment.objects.get(id=cs["comment"]["id"])
            self.assertEqual(cs["comment"]["message"], real_comment.message)
            self.assertEqual(cs["comment"]["user"], real_comment.user.id)
        self.assertIsNotNone(CommentAlbum.objects.get(id=response.json()[0]["album_id"]))
        self.assertIsNotNone(CommentAlbum.objects.get(id=response.json()[1]["album_id"]))
        self.assertIsNotNone(CommentAlbum.objects.get(id=response.json()[2]["album_id"]))

    def test_get_all_album_comments_other_user(self):
        response = self.client_other.get(reverse('comment_album-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertIsNotNone(CommentAlbum.objects.get(id=response.json()[0]["album_id"]))
        self.assertIsNotNone(CommentAlbum.objects.get(id=response.json()[1]["album_id"]))

    def test_get_all_album_comments_of_specific_album(self):
        self.make_comment(self.user,  self.album)
        self.make_comment(self.user,  self.album)
        response = self.client.get(reverse('comment_album-list')+f"?album={self.album.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        for cs in response.json():
            self.assertEqual(cs["album_id"], self.album.id)
        response = self.client.get(reverse('comment_album-list') + f"?album={self.album_other.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        for cs in response.json():
            self.assertEqual(cs["album_id"], self.album_other.id)

    def test_other_user_tries_to_get_private_info(self):
        response = self.client_other.get(reverse('comment_album-list') + f"?album={self.album_private.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)


    def test_unauthenticated_user_can_view_coments(self):
        response = self.client_unauthenticated.get(reverse('comment_album-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
