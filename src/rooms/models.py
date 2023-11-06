from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from thermo.settings import AUTH_USER_MODEL


class Room(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rooms')

    def save(self, *args, **kwargs):
        """
        Save the new room with a unique slug
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Room, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("room", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.name}"


class Device(models.Model):
    TYPE_CHOICES = [
        ("light", "capteur de luminosité"),
        ("temperature", "capteur de température"),
        ("appliance", "capteur de consommation"),
    ]

    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128, choices=TYPE_CHOICES)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='devices')

    def create_lighting(self, brightness_outside: float, brightness_inside: float,
                        brightness_desired: float = None) -> None:
        Lighting.objects.create(
            brightness_outside=brightness_outside,
            brightness_inside=brightness_inside,
            brightness_desired=brightness_desired,
            devices=self,
        )

    def create_heating(self, temperature_outside: float, temperature_inside: float,
                       temperature_desired: float = None) -> None:
        Heating.objects.create(
            temperature_outside=temperature_outside,
            temperature_inside=temperature_inside,
            temperature_desired=temperature_desired,
            devices=self,
        )

    def __str__(self):
        return f"{self.name} - {self.type}"


class Lighting(models.Model):
    brightness_outside = models.FloatField()
    brightness_inside = models.FloatField()
    brightness_desired = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    devices = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='lightings')

    def __str__(self):
        return f"Brightness inside: {self.brightness_inside}lm ({self.timestamp})"


class Heating(models.Model):
    temperature_outside = models.FloatField()
    temperature_inside = models.FloatField()
    temperature_desired = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    devices = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='heating')

    def __str__(self):
        return f"Temperature inside: {self.temperature_inside}°C ({self.timestamp})"


class HomeAppliance(models.Model):
    mode = models.CharField(max_length=128)
    power = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    devices = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='HomeAppliances')

    def __str__(self):
        return f"{self.mode}-{self.power} ({self.timestamp})"


class Notification(models.Model):
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    devices = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"{self.id}: {self.content} ({self.timestamp})"
