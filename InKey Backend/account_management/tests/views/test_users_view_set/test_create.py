from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin


class TestCreateUserView(TestUserMixin):
    def test_create_user_unauthenticated_user(self):
        response = self.client_unauthenticated.post(reverse("user-list"), {
            "email": "newuser@mail.com",
            "firstname": "first",
            "lastname": "last",
            "password": "haha",
        })
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json()["email"], "newuser@mail.com")
        self.assertEqual(response.json()["settings"]["theme"], 1)

    def test_create_user_authenticated_user(self):
        response = self.client.post(reverse("user-list"), {
            "email": "newuser@mail.com",
            "firstname": "first",
            "lastname": "last",
            "password": "haha",
        })
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json()["email"], "newuser@mail.com")
        self.assertEqual(response.json()["settings"]["theme"], 1)

    def test_create_user_with_same_email(self):
        response = self.client.post(reverse("user-list"), {
            "email": self.user.email,
            "firstname": "first",
            "lastname": "last",
            "password": "haha",
        })
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_user_together_with_settings(self):
        response = self.client.post(reverse("user-list"), {
            "email": "newuser@mail.com",
            "firstname": "first",
            "lastname": "last",
            "password": "haha",
            "settings.theme": 2
        })
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json()["email"], "newuser@mail.com")
        self.assertEqual(response.json()["settings"]["theme"], 1)

    def test_create_user_is_not_active_should_not_make_user_not_active(self):
        response = self.client.post(reverse("user-list"), {
            "email": "newuser@mail.com",
            "firstname": "first",
            "lastname": "last",
            "password": "haha",
            "is_active": False,
            "is_staff": True,
        })
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json()["email"], "newuser@mail.com")
        self.assertEqual(response.json()["settings"]["theme"], 1)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
