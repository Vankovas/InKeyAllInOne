from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db import models
from account_management.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from annoying.fields import AutoOneToOneField


def profile_picture_path(instance, filename):
    email = instance.email.replace(".", "_")
    email = email.replace("@", "_")
    return f'user_{email}/{filename}'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    firstname = models.CharField(max_length=64, default=None, null=True, blank=True)
    lastname = models.CharField(max_length=64, default=None, null=True, blank=True)
    username = models.CharField(max_length=64, default=None, null=True, blank=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to=profile_picture_path, null=True, default=None,
                                        storage=MediaCloudinaryStorage())
    description = models.CharField(max_length=1024, default="", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.firstname is None:
            return ""
        else:
            return self.firstname + " " + self.lastname


class UserSettings(models.Model):
    theme = models.IntegerField(default=1)
    user = AutoOneToOneField("account_management.User", on_delete=models.CASCADE, related_name="settings")
