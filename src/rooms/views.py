from django.shortcuts import render, get_object_or_404
import random

from rooms.models import Room


def room(request, slug):

    room = get_object_or_404(Room, slug=slug)

    datapoints = []
    datapoints2 = []
    count, y = 24, 5

    for i in range(count):
        y += round(5 + random.uniform(-5, 5))
        datapoints.append({"x": i, "y": y})
        datapoints2.append({"x": i+2, "y": y-3})

    context = {
        "room": room,
        "datapoints": datapoints,
        "datapoints2": datapoints2,
    }

    return render(request, 'rooms/room.html', context=context)
