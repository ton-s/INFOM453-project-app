from django.shortcuts import render
import requests

from rooms.models import Room


def index(request):

    # key = "3448cb1dd62b9758038f490877c25fb6"
    # url = f"http://api.weatherstack.com/current?access_key={key}&query=Gedinne"
    #
    #
    # data = requests.get(url).json()
    #
    # print(data)

    rooms = Room.objects.all()

    return render(request, 'core/home.html', context={'rooms': rooms})
