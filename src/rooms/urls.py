from django.urls import path

from rooms.views import room, decrease_temperature, increase_temperature, change_brightness

urlpatterns = [
    path("", room, name='room'),
    path("decrease-temperature/", decrease_temperature, name="decrease_temperature"),
    path("increase-temperature/", increase_temperature, name="increase_temperature"),
    path("change-brightness/", change_brightness, name="change_brightness"),
]