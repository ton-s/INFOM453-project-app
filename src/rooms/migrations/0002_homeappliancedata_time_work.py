# Generated by Django 4.2.6 on 2023-11-14 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeappliancedata',
            name='time_work',
            field=models.FloatField(default=''),
            preserve_default=False,
        ),
    ]
