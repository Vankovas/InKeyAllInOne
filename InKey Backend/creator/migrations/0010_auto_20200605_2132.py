# Generated by Django 2.2.6 on 2020-06-05 19:32

import cloudinary_storage.storage
import creator.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0009_auto_20200605_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover_image',
            field=models.ImageField(blank=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to=creator.models.cover_path, validators=[creator.models.validate_image_extension]),
        ),
    ]