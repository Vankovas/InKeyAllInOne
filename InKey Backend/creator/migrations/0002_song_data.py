# Generated by Django 2.2.6 on 2020-04-18 10:53

import creator.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='data',
            field=models.FileField(null=True, upload_to=creator.models.song_path, validators=[creator.models.validate_file_extension]),
        ),
    ]
