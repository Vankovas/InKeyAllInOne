# Generated by Django 2.2.6 on 2020-06-05 17:56

import account_management.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_management', '0002_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(null=True, storage='django.core.files.storage.FileSystemStorage', upload_to=account_management.models.profile_picture_path),
        ),
    ]