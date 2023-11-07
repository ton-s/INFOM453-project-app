# Generated by Django 4.2.6 on 2023-11-07 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Heating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomeAppliance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lighting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=512)),
                ('action', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('heating', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='heating_notifications', to='rooms.lighting')),
                ('lighting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lighting_notifications', to='rooms.lighting')),
            ],
        ),
        migrations.CreateModel(
            name='LightingData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brightness_outside', models.FloatField()),
                ('brightness_inside', models.FloatField()),
                ('brightness_desired', models.FloatField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('lighting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lighting_data', to='rooms.lighting')),
            ],
        ),
        migrations.AddField(
            model_name='lighting',
            name='room',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='d_lighting', to='rooms.room'),
        ),
        migrations.CreateModel(
            name='HomeApplianceData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(max_length=128)),
                ('power', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('homeAppliance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeAppliances_data', to='rooms.homeappliance')),
            ],
        ),
        migrations.AddField(
            model_name='homeappliance',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='d_homeAppliance', to='rooms.room'),
        ),
        migrations.CreateModel(
            name='HeatingData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature_outside', models.FloatField()),
                ('temperature_inside', models.FloatField()),
                ('temperature_desired', models.FloatField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('heating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heating_data', to='rooms.heating')),
            ],
        ),
        migrations.AddField(
            model_name='heating',
            name='room',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='d_heating', to='rooms.room'),
        ),
    ]