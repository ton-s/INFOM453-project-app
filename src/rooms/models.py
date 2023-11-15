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
    name = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id} - {self.name}"


class Lighting(Device):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='d_lighting')

    def save_data(self, brightness_outside, brightness_inside, brightness_desired=None):
        LightingData.objects.create(brightness_outside=brightness_outside,
                                    brightness_inside=brightness_inside,
                                    brightness_desired=brightness_desired,
                                    lighting=self)


class LightingData(models.Model):
    brightness_outside = models.FloatField()
    brightness_inside = models.FloatField()
    brightness_desired = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    lighting = models.ForeignKey(Lighting, on_delete=models.CASCADE, related_name='lighting_data')

    def change_brightness(self, value):
        self.brightness_desired = value
        self.brightness_inside = value
        self.save()

        return self.brightness_desired

    @staticmethod
    def convert_lumen_to_percent(value):
        max_lumen = 250
        result = int((value / max_lumen) * 100)
        return result

    @staticmethod
    def convert_percent_to_lum(value):
        max_lumen = 250
        result = (value / 100) * max_lumen
        return result

    def __str__(self):
        return f"Brightness inside: {self.brightness_inside}lm ({self.timestamp}) ({self.id})"


class Heating(Device):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='d_heating')

    def save_data(self, temperature_outside, temperature_inside, temperature_desired=None):
        HeatingData.objects.create(temperature_outside=temperature_outside,
                                   temperature_inside=temperature_inside,
                                   temperature_desired=temperature_desired,
                                   heating=self)


class HeatingData(models.Model):
    temperature_outside = models.FloatField()
    temperature_inside = models.FloatField()
    temperature_desired = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    heating = models.ForeignKey(Heating, on_delete=models.CASCADE, related_name='heating_data')

    def increase(self):
        if self.temperature_desired < 30:
            self.temperature_desired += 1
            self.save()

        return self.temperature_desired

    def decrease(self):
        if self.temperature_desired > 0:
            self.temperature_desired -= 1
            self.save()

        return self.temperature_desired

    def __str__(self):
        return f"Temperature inside: {self.temperature_inside}°C ({self.timestamp}) ({self.id})"


class HomeAppliance(Device):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='d_homeAppliance')

    def save_data(self, mode, power, time_work):
        HomeApplianceData.objects.create(mode=mode,
                                         power=power,
                                         time_work=time_work,
                                         homeAppliance=self)


class HomeApplianceData(models.Model):
    mode = models.CharField(max_length=128)
    power = models.FloatField()
    time_work = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    homeAppliance = models.ForeignKey(HomeAppliance, on_delete=models.CASCADE, related_name='homeAppliances_data')

    def __str__(self):
        return f"{self.mode}-{self.power}-{self.time_work} ({self.timestamp}) ({self.id})"


class Notification(models.Model):
    content = models.CharField(max_length=512)
    action = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    lighting = models.ForeignKey(Lighting, on_delete=models.CASCADE, related_name='lighting_notifications',
                                 blank=True,
                                 null=True)
    heating = models.ForeignKey(Heating, on_delete=models.CASCADE, related_name='heating_notifications',
                                blank=True,
                                null=True)

    def __str__(self):
        return f"{self.id}: {self.content} ({self.timestamp})"
