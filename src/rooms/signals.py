from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from core.consumers import CoreConsumer
from core.utils import run_model_heating
from rooms.models import Room, Heating, Lighting, HomeAppliance, HeatingData, LightingData, Notification


# SETUP DB
@receiver(post_save, sender=CustomUser)
def create_rooms(sender, instance, created, **kwargs):
    """Creation of Room instances when creating a superuser"""

    if created and instance.is_superuser:
        # Rooms
        bedroom = Room.objects.create(name="chambre", user=instance)
        salon = Room.objects.create(name="salon", user=instance)
        kitchen = Room.objects.create(name="cuisine", user=instance)
        bathroom = Room.objects.create(name="salle de bain", user=instance)

        # Devices
        for r in [bedroom, salon, kitchen, bathroom]:
            Heating.objects.create(name="phidget_temperature", room=r)
            Lighting.objects.create(name="phidget_light", room=r)

        HomeAppliance.objects.create(name="machine-a-laver", room=bathroom)


@receiver(post_save, sender=HeatingData)
def update_temperature_desired(sender, instance, created, **kwargs):
    """Update temperature_desired after adding a new line to HeatingData"""

    if created and instance.temperature_desired is None:
        last_temperature = sender.objects.filter(heating_id=instance.heating_id).exclude(id=instance.id).last()
        if last_temperature:
            if instance.temperature_inside != last_temperature.temperature_desired:
                instance.temperature_desired = last_temperature.temperature_desired
        else:
            instance.temperature_desired = instance.temperature_inside

        instance.save()


@receiver(post_save, sender=LightingData)
def update_brightness_desired(sender, instance, created, **kwargs):
    """Update brightness_desired after adding a new line to LightingData"""

    if created and instance.brightness_desired is None:
        instance.brightness_desired = instance.brightness_inside
        instance.save()


@receiver(post_save, sender=LightingData)
def send_message_brightness(sender, instance, created, **kwargs):
    """Send message to device when brightness changes"""

    last_lighting = sender.objects.filter(lighting_id=instance.lighting_id).exclude(id=instance.id).last()

    if not created and last_lighting:

        if float(last_lighting.brightness_inside) != float(instance.brightness_inside):
            message = dict()
            message[instance.lighting.room.slug] = {"light": instance.brightness_inside,
                                                    "curtains": instance.open_curtains}

            print(f"Data sent: {message}")

            # send data to devices
            consumer = CoreConsumer()
            consumer.send_message(message)


# ALGORITHME
@receiver(post_save, sender=HeatingData)
def heating_detection_algorithm(sender, instance, created, **kwargs):
    """Algorithm for detecting the ideal temperature in a room"""

    if not created:
        last_heating = sender.objects.filter(heating_id=instance.heating_id).exclude(id=instance.id).last()
        print(last_heating)
        if last_heating:
            prediction = run_model_heating(instance)
            print(prediction)

            # create notification
            content = f"Salut, c'est moi !\nJe souhaite changer la température de ton chauffage à {prediction}°C"
            action = (prediction - float(instance.temperature_desired))
            context = {"content": content, "action": action, "heating": instance.heating}

            last_instance, create = Notification.objects.get_or_create(heating=instance.heating, defaults=context)

            if not create:
                last_instance.__dict__.update(**context)
                last_instance.save()

            #TODO - mettre une régle pour limiter l'envoie de notif
@receiver(post_save, sender=HeatingData)
def lighting_detection_algorithm(sender, instance, created, **kwargs):
    """Algorithm for detecting the ideal brightness in a room"""
    pass
