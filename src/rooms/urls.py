from django.urls import path

from rooms.views import room

urlpatterns = [
    path("room/<str:slug>/", room, name='room'),
]