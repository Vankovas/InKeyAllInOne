from django.urls import reverse

from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album
from user.models import CommentAlbum, Comment


class TestCreateCommentOnAlbum(TestUserMixin):
    def setUp(self) -> None:
        super(TestCreateCommentOnAlbum, self).setUp()
        self.album = Album.objects.create(name="yes1", artist=self.user)
        self.album_other = Album.objects.create(name="yes2", artist=self.user_other)
        self.creation_data = {
            'comment': {
                "message": "hey you sux"
            },
            "album_id": self.album.id
        }

    def assert_create_is_correct(self, response, album, user):
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CommentAlbum.objects.count(), 1)
        self.assertEqual(CommentAlbum.objects.get().comment, Comment.objects.get())
        self.assertEqual(CommentAlbum.objects.get().album, album)
        self.assertEqual(CommentAlbum.objects.get().comment.user.id, user.id)

    def test_create_comment_works(self):
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CommentAlbum.objects.count(), 0)
        response = self.client.post(reverse('comment_album-list'), data=self.creation_data, format='json')
        self.assert_create_is_correct(response, self.album, self.user)

    def test_create_comment_with_non_existing_album_doesnt_work(self):
        self.creation_data["album_id"] = -1
        response = self.client.post(
            reverse('comment_album-list'),
            data=self.creation_data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()[0], 'Enter a correct album id!!!')

    def test_create_comment_on_another_persons_album_works(self):
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CommentAlbum.objects.count(), 0)
        self.creation_data["album_id"] = self.album_other.id
        response = self.client.post(reverse('comment_album-list'), data=self.creation_data, format='json')
        self.assert_create_is_correct(response, self.album_other, self.user)

    def test_create_comment_not_logged_in_doesnt_work(self):
        response = self.client_unauthenticated.post(
            reverse('comment_album-list'),
            data=self.creation_data,
            format='json'
        )
        self.assertEqual(response.status_code, 401)

    def test_create_comment_twice_works(self):
        response = self.client.post(reverse('comment_album-list'), data=self.creation_data, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse('comment_album-list'), data=self.creation_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(CommentAlbum.objects.count(), 2)
        for cs in CommentAlbum.objects.all():
            self.assertEqual(cs.album, self.album)
            self.assertEqual(cs.comment.user.id, self.user.id)

    def test_create_comment_on_private_album_which_doesnt_belong_to_you_doesnt_work(self):
        album = Album.objects.create(name="private", artist=self.user_other, is_private=True)
        self.creation_data["album_id"] = album.id
        response = self.client.post(reverse('comment_album-list'), data=self.creation_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CommentAlbum.objects.count(), 0)

    def test_create_comment_on_private_album_which_belongs_to_you_works(self):
        album = Album.objects.create(name="private", artist=self.user, is_private=True)
        self.creation_data["album_id"] = album.id
        response = self.client.post(reverse('comment_album-list'), data=self.creation_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assert_create_is_correct(response, album, self.user)

