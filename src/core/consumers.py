import json

import channels.layers
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from core.utils import get_weather_data
from rooms.models import Room

GROUPE = "devices"


class CoreConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        # Join group
        async_to_sync(self.channel_layer.group_add)(
            GROUPE, self.channel_name
        )

    def disconnect(self, close_code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            GROUPE, self.channel_name
        )

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

                last_light_data = room.d_lighting.lighting_data.last()
                current_brightness_inside = last_light_data.brightness_inside if last_light_data else 0

                if "homeappliance" in data[slug]:
                    if any(data[slug]["homeappliance"]):
                        for homeappliance in room.d_homeAppliance.all():
                            machine = data[slug]["homeappliance"][homeappliance.name]
                            homeappliance.save_data(mode=machine[0],
                                                    power=machine[1],
                                                    time_work=machine[2])

                # Save data
                room.d_lighting.save_data(brightness_outside=current_brightness_outside,
                                          brightness_inside=current_brightness_inside)
                room.d_heating.save_data(temperature_outside=current_temperature_outside,
                                         temperature_inside=current_temperature_inside)

    def send_message(self, message):
        # Send message to group
        channels_layer = channels.layers.get_channel_layer()
        async_to_sync(channels_layer.group_send)(
            GROUPE, {"type": "type.message", "message": message}
        )

    def type_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps(message))
