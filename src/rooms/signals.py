from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from rooms.models import Room, Device


@receiver(post_save, sender=CustomUser)
def create_rooms(sender, instance, created, **kwargs):
    # creation of Room instances when creating a superuser
    if created and instance.is_superuser:
        # Rooms
        bedroom = Room.objects.create(name="chambre", user=instance)
        salon = Room.objects.create(name="salon", user=instance)
        kitchen = Room.objects.create(name="cuisine", user=instance)
        bathroom = Room.objects.create(name="salle de bain", user=instance)

        # Devices
        Device.objects.create(name="phidget_temperature", type="temperature", room=salon)