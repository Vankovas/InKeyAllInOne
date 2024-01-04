from http import HTTPStatus
from django.urls import reverse

from account_management.models import User
from account_management.tests.mixin.test_user_mixin import TestUserMixin


class TestDeleteUserView(TestUserMixin):
    def test_delete_user_unauthenticated_user(self):
        response = self.client_unauthenticated.delete(reverse("user-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_delete_user_himself(self):
        pk = self.user.pk
        response = self.client.delete(reverse("user-detail", kwargs={"pk": pk}))
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(User.objects.filter(pk=pk).count(), 0)

    def test_delete_user_another_user(self):
        pk = self.user_other.pk
        response = self.client.delete(reverse("user-detail", kwargs={"pk": pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(User.objects.filter(pk=pk).count(), 1)
