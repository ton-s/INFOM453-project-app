from django.urls import path

from rooms.views import room, decrease_temperature, increase_temperature

urlpatterns = [
    path("room/<str:slug>/", room, name='room'),
    path("room/<str:slug>/decrease-temperature", decrease_temperature, name="decrease_temperature"),
    path("room/<str:slug>/increase-temperature", increase_temperature, name="increase_temperature")
]