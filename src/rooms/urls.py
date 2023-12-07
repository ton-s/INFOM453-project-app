from django.urls import path

from rooms.views import room, decrease_temperature, increase_temperature, change_brightness, notification_valid, \
    notification_close

urlpatterns = [
    path("", room, name='room'),
    path("decrease-temperature/", decrease_temperature, name="decrease_temperature"),
    path("increase-temperature/", increase_temperature, name="increase_temperature"),
    path("change-brightness/", change_brightness, name="change_brightness"),
    path("notification-valid/<int:notification_id>/", notification_valid, name="notification_valid"),
    path("notification-close/<int:notification_id>/", notification_close, name="notification_close"),
]
