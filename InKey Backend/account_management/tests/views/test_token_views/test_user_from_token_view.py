from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin


class TestGetUserFromTokenView(TestUserMixin):
    def test_get_unauthenticated_user(self):
        response = self.client_unauthenticated.get(reverse("token_info"))
        print(response.json())
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_get_authenticated_user(self):
        response = self.client.get(reverse("token_info"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        user = response.json()
        settings = user["settings"]
        del user["settings"]
        for key in user:
            self.assertEqual(getattr(self.user, key, None), user[key])
        for key in settings:
            self.assertEqual(getattr(self.user.settings, key, None), settings[key])

    def test_get_user_with_another_header_returns_another_user(self):
        response = self.client_other.get(reverse("token_info"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(response.json()["email"], self.user.email)
        self.assertEqual(response.json()["email"], self.user_other.email)
