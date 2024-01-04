from http import HTTPStatus
from django.urls import reverse

from account_management.models import User
from account_management.tests.mixin.test_user_mixin import TestUserMixin


class TestUpdateUserView(TestUserMixin):
    def test_update_user_unauthenticated_user(self):
        response = self.client_unauthenticated.patch(
            reverse("user-detail", kwargs={"pk": self.user.pk}),
            {
                "username": "username"
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_update_user_himself(self):
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": self.user.pk}),
            {
                "username": "newer username"
            }
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.user.username, "newer username")

    def test_update_user_another_user(self):
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": self.user_other.pk}),
            {
                "username": "newer username"
            }
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertNotEqual(self.user_other.username, "newer username")

    def test_update_user_all_fields(self):
        self.assertEqual(self.user.settings.theme, 1)
        self.assertFalse(bool(self.user.profile_picture))
        new_data = {
            "username": "new username",
            "firstname": "new firstname",
            "lastname": "new lastname",
            "email": "newer_mail@email.com",
            "settings.theme": 2,
            "profile_picture": self.get_image_for_upload()
        }
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": self.user.pk}),
            new_data
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.user.settings.theme, 2)
        self.assertTrue(bool(self.user.profile_picture))
        new_data.pop("settings.theme")
        new_data.pop("profile_picture")
        for key in new_data:
            self.assertEqual(getattr(self.user, key, None), new_data[key])

    def test_update_user_settings_cannot_update_settings_user_immutable_fields(self):
        self.assertEqual(self.user.settings.theme, 1)
        original_settings = self.user.settings.pk
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": self.user.pk}),
            {
                "settings.theme": 121,
                "settings.user": self.user_other.pk,
                "settings.id": self.user_other.settings.pk+1,
            }
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.user.settings.pk, original_settings)

    def test_update_user_cannot_just_give_new_update_password(self):
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": self.user.pk}),
            {
                "new_password": "haha",
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password("haha"))

    def test_update_user_cannot_update_password_with_wrong_confirm(self):
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": self.user.pk}),
            {
                "new_password": "haha",
                "confirm_new_password": "haha1",
                "password": "yes",
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password("haha"))

    def test_update_user_can_update_password(self):
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": self.user.pk}),
            {
                "new_password": "haha",
                "confirm_new_password": "haha",
                "password": "yes",
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("haha"))

