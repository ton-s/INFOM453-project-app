from django.shortcuts import render, get_object_or_404
import random

from django.utils import timezone

from rooms.models import Room, Lighting


def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    heating_data = room.d_heating.heating_data
    lighting_data = room.d_lighting.lighting_data
    today = timezone.now().date()

    # chart_data_1 = []
    # chart_data_1_threshold = []
    # count, y = 24, 5
    #
    # for i in range(count):
    #     y += round(5 + random.uniform(-5, 5))
    #     chart_data_1.append({"x": i, "y": y})
    #     chart_data_1_threshold.append({"x": i + 2, "y": y - 3})

    chart_data_1 = []
    chart_data_1_threshold = []
    # chart_data_2 = []

    for data in heating_data.filter(timestamp__date=today):
        chart_data_1.append({"x": int(data.timestamp.timestamp()), "y": data.temperature_inside})
        chart_data_1_threshold.append({"x": int(data.timestamp.timestamp()), "y": data.temperature_outside})
    print(chart_data_1)
    context = {
        "room": room,
        "temperature_outside": int(heating_data.last().temperature_outside),
        "temperature_inside": int(heating_data.last().temperature_inside),
        "brightness_outside": int(lighting_data.last().brightness_outside),
        "brightness_inside": int(lighting_data.last().brightness_inside),
        "chart_data_1": chart_data_1,
        "chart_data_1_threshold": chart_data_1_threshold,
        "chart_data_2": [{}],
    }

    return render(request, 'rooms/room.html', context=context)
