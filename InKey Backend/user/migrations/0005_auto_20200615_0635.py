# Generated by Django 2.2.6 on 2020-06-15 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200605_0204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist',
            old_name='artist',
            new_name='user',
        ),
    ]
