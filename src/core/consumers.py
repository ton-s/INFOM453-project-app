import json

from channels.generic.websocket import AsyncWebsocketConsumer

from core.utils import get_weather_data
from rooms.models import Room, Device


class CoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print(text_data_json)

        await self.save_data(text_data_json)

    async def save_data(self, data: dict):
        temperature = data["temperature"]
        light = data["light"]

        room = await Room.objects.get(slug="salon")
        await Device.create_lighting(brightness_outside=get_weather_data(),
                                     brightness_inside=temperature.value)



