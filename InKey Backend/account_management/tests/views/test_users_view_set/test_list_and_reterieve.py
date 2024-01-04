from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin


class TestListAndRetrieveUserView(TestUserMixin):
    def test_list_user_unauthenticated_user(self):
        response = self.client_unauthenticated.get(reverse("user-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), 2)

    def test_retrieve_user_unauthenticated_user(self):
        response = self.client_unauthenticated.get(reverse("user-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()["email"],self.user.email)

    def test_list_user_authenticated_user(self):
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), 2)

    def test_retrieve_user_authenticated_user(self):
        response = self.client.get(reverse("user-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()["email"], self.user.email)