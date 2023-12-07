from django.urls import path

from core.views import index, change_night_mode

urlpatterns = [
    path('', index, name='index'),
    path('change-night-mode/', change_night_mode, name='change_night_mode'),
]
