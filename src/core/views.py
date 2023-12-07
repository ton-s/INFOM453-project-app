from django.http import HttpResponseBadRequest
from django.shortcuts import render, HttpResponse

from core.utils import get_weather_data, get_season_now
from rooms.models import Room


def index(request):
    weather = get_weather_data()
    season = get_season_now()
    rooms = Room.objects.all()

    all_rooms_night_mode = all(room.night_mode for room in rooms)

    return render(request, 'core/home.html', context={'rooms': rooms, 'weather': weather, 'season': season,
                                                      'all_rooms_night_mode': all_rooms_night_mode})


def change_night_mode(request):
    if request.method == "POST":
        rooms = Room.objects.all()

        for room in rooms:
            room.toggle_mode()

        all_rooms_night_mode = all(room.night_mode for room in rooms)

        if all_rooms_night_mode:
            return HttpResponse('<div><i class="fa-regular fa-moon fa-xl night"></i></div>')

        else:
            return HttpResponse('<div><i class="fa-solid fa-sun fa-xl day"></i></div>')

    else:
        # Indicates that the request is not allowed
        return HttpResponseBadRequest("Méthode non autorisée")
