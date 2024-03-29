from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from thermo.settings import AUTH_USER_MODEL


class Room(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    night_mode = models.BooleanField(default=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rooms')

    def toggle_mode(self):
        """Toggle the night mode status
        """
        self.night_mode = not self.night_mode
        self.save()

        last_lighting_data = self.d_lighting.lighting_data.last()
        if self.night_mode:
            _ = last_lighting_data.change_brightness(0, True)
        else:
            _ = last_lighting_data.change_brightness(20)

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
    brightness_outside = models.FloatField()  # lux
    brightness_inside = models.FloatField()  # lumen
    brightness_desired = models.FloatField(blank=True, null=True)  # lumen
    close_curtains = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    lighting = models.ForeignKey(Lighting, on_delete=models.CASCADE, related_name='lighting_data')

    MAX_BRIGHTNESS_INSIDE = 250  # lumen
    MAX_BRIGHTNESS_OUTSIDE = 10000  # lux

    def change_brightness(self, value, curtains=False):
        self.brightness_desired = value
        self.brightness_inside = value
        self.close_curtains = curtains
        self.save()

        return self.brightness_desired

    def set_curtains(self, value):
        self.close_curtains = value
        self.save()

    def get_type_brightness(self):
        """Get an outdoor brightness type

        Return
        ------
        type_brightness (string) : an outdoor brightness type
        """
        # brightness outside in lux
        if self.brightness_outside <= 20:
            type_brightness = "Nuit"
        elif 20 < self.brightness_outside <= 500:
            type_brightness = "Sombre"
        elif 500 < self.brightness_outside <= 3000:
            type_brightness = "Nuageux"
        else:
            type_brightness = "Soleil"

        return type_brightness

    @staticmethod
    def convert_lumen_to_percent(value):
        """Converts a lumen value to its percentage relative to the maximum brightness inside

        Parameters
        ----------
        value (float) : the lumen value to be converted

        Return
        ------
        result (int) : the percentage of the given lumen value relative to the maximum brightness inside
        """
        max_lumen = LightingData.MAX_BRIGHTNESS_INSIDE
        result = int((value / max_lumen) * 100)
        return result

    @staticmethod
    def convert_percent_to_lum(value):
        """Converts a percentage value to the corresponding lumen value relative to the maximum brightness inside

        Parameters
        ----------
        value (float) : the percentage value to be converted
        Return
        ------
        result (int) : the lumen value equivalent to the given percentage relative to the maximum brightness inside
        """
        max_lumen = LightingData.MAX_BRIGHTNESS_INSIDE
        result = (value / 100) * max_lumen
        return result

    @staticmethod
    def convert_lux_to_percent(value):
        """Converts a lux value to its percentage relative to the maximum brightness outside

        Parameters
        ----------
        value (float): the lux value to be converted

        Return
        ------
        result (int) : the percentage of the given lux value relative to the maximum brightness outside
        """
        max_lux = LightingData.MAX_BRIGHTNESS_OUTSIDE  # full sun
        result = int((value / max_lux) * 100)
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

    def set_temperature_desired(self, value):
        new_temperature = self.temperature_desired + value
        self.temperature_desired = new_temperature if 0 <= new_temperature <= 30 else 0 if new_temperature < 0 else 30
        self.save()

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
