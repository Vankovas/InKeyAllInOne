# Generated by Django 2.2.6 on 2020-06-17 00:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_remove_stream_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 6, 17, 2, 34, 38, 144595)),
            preserve_default=False,
        ),
    ]
