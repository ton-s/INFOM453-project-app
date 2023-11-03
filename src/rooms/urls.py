from django.urls import path

from rooms.views import room

urlpatterns = [
    path("room/<str:room_name>/", room, name='room'),
]