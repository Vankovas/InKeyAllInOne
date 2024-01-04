# Generated by Django 2.2.6 on 2020-06-13 18:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0013_auto_20200613_2006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='albumvote',
            old_name='song',
            new_name='album',
        ),
        migrations.AlterField(
            model_name='album',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 13, 20, 34, 40, 447857)),
        ),
        migrations.AlterField(
            model_name='song',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 13, 20, 34, 40, 448856)),
        ),
    ]
