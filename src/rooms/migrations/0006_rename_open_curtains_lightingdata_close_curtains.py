# Generated by Django 4.2.6 on 2023-12-08 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_room_night_mode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lightingdata',
            old_name='open_curtains',
            new_name='close_curtains',
        ),
    ]
