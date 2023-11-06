import json

from channels.generic.websocket import WebsocketConsumer

from core.utils import get_weather_data
from rooms.models import Room, Device


class CoreConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print(text_data_json)

        self.save_data(text_data_json)

    def save_data(self, data: dict):
        current_temperature_inside = data["temperature"]["value"]
        current_temperature_outside = get_weather_data()["current"]["temperature"]
        current_brightness_outside = data["light"]["value"]

        room = Room.objects.get(slug="salon")
        device = Device.objects.get(room=room)
        device.create_lighting(brightness_outside=current_brightness_outside,
                               brightness_inside="100")
        device.create_heating(temperature_outside=current_temperature_outside,
                              temperature_inside=current_temperature_inside)
