from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from core.consumers import CoreConsumer
from core.utils import run_model_heating, run_model_lighting
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

        if last_heating:
            # add a bias to the algorithm trigger
            temp_change_outside = abs(float(instance.temperature_outside) - last_heating.temperature_outside)
            temp_change_inside = abs(float(instance.temperature_inside) - last_heating.temperature_inside)
            temp_change_desired = abs(float(instance.temperature_desired) - last_heating.temperature_desired)

            if temp_change_outside > 2 or temp_change_inside > 2 or temp_change_desired > 2:

                prediction = run_model_heating(instance)
                # print(last_heating)
                # print(prediction)

                # create a heating notification
                content = f"Salut, c'est moi !\nJe souhaite changer la température de ton chauffage à {prediction}°C"
                action = (prediction - float(instance.temperature_desired))
                context = {"content": content, "action": action, "heating": instance.heating}

                last_instance, create = Notification.objects.get_or_create(heating=instance.heating, defaults=context)

                if not create:
                    last_instance.__dict__.update(**context)
                    last_instance.save()


@receiver(post_save, sender=LightingData)
def lighting_detection_algorithm(sender, instance, created, **kwargs):
    """Algorithm for detecting the ideal brightness in a room"""

    if not created:
        last_lighting = sender.objects.filter(lighting_id=instance.lighting_id).exclude(id=instance.id).last()

        if last_lighting:
            # add a bias to the algorithm trigger
            brightness_change_outside = abs(float(instance.brightness_outside) - last_lighting.brightness_outside)
            brightness_change_inside = abs(float(instance.brightness_inside) - last_lighting.brightness_inside)

            if brightness_change_outside >= (LightingData.MAX_BRIGHTNESS_OUTSIDE * 0.2) \
                    or brightness_change_inside >= (LightingData.MAX_BRIGHTNESS_INSIDE * 0.1):

                prediction = run_model_lighting(instance)
                print(last_lighting)
                print(f"Lighting: {prediction}")

                # create a lighting notification
                content = f"Salut, c'est moi !\nJe souhaite changer la luminosité de la pièce à {prediction}"
                action = prediction
                context = {"content": content, "action": action, "lighting": instance.lighting}

                last_instance, create = Notification.objects.get_or_create(lighting=instance.lighting, defaults=context)

                if not create:
                    last_instance.__dict__.update(**context)
                    last_instance.save()
