from django.db import models
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
