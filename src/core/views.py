from django.shortcuts import render

from core.utils import get_weather_data
from rooms.models import Room


def index(request):
    weather = get_weather_data()

    rooms = Room.objects.all()

    return render(request, 'core/home.html', context={'rooms': rooms, 'weather': weather})
