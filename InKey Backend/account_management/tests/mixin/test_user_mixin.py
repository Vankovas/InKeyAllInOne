from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.test import TestCase


class TestUserMixin(TestCase):
    def setUp(self) -> None:
        self.User = get_user_model()
        self.user = self.create_user(email="newmail@mail.com", password="yes")
        self.client = self.get_authenticated_client(email="newmail@mail.com", password="yes")
        self.user_other = self.create_user(email="newmail2@mail.com", password="yes2")
        self.client_other = self.get_authenticated_client(email="newmail2@mail.com", password="yes2")
        self.client_unauthenticated = APIClient()

    def create_user(self, email, password, **kwargs):
        user = self.User.objects.create(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def get_authenticated_client(email, password):
        client = APIClient()
        response = client.post(
            reverse("login"), {"email": email, "password": password}
        )
        json_content = response.json()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + json_content["access"])
        return client

    @staticmethod
    def get_image_for_upload():
        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        image_name = get_random_string(length=10) + ".gif"
        image = SimpleUploadedFile(image_name, testfile, content_type="image/gif")
        return image

    @staticmethod
    def get_wav_audio_for_upload():
        testfile = (
            b"RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00\x04"
            b"\x00\x00\x00\x04\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00"
        )
        audio_name = get_random_string(length=10) + ".wav"
        wav = SimpleUploadedFile(audio_name, testfile, content_type="audio/x-wav")
        return wav

