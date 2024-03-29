# Generated by Django 2.2.6 on 2020-06-13 20:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0014_auto_20200613_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='song',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='album',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 13, 22, 43, 3, 392894)),
        ),
        migrations.AlterField(
            model_name='song',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 13, 22, 43, 3, 393895)),
        ),
    ]
