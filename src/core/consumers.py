import json

from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404

from core.utils import get_weather_data
from rooms.models import Room


class CoreConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print(text_data_json)

        self.save_data_in_database(text_data_json)

    def save_data_in_database(self, data):
        """Save sensor data in the database

        Parameters
        ----------
        data (dict): sensor data
        """

        rooms = Room.objects.all()

        # Get the current temperature via the weather api
        current_temperature_outside = get_weather_data()["current"]["temperature"]

        for room in rooms:
            slug = room.slug

            if slug in data:
                # Get data
                current_brightness_outside = data[slug]["light"]
                current_temperature_inside = data[slug]["temperature"]

                if "homeappliance" in data[slug]:
                    for homeappliance in room.d_homeAppliance.all():
                        homeappliance.save_data(mode=data[slug]["homeappliance"][homeappliance.name][0],
                                                power=data[slug]["homeappliance"][homeappliance.name][1])

                # Save data
                room.d_lighting.save_data(brightness_outside=current_brightness_outside,
                                          brightness_inside="100")
                room.d_heating.save_data(temperature_outside=current_temperature_outside,
                                         temperature_inside=current_temperature_inside)
