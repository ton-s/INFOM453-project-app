from django.shortcuts import render, get_object_or_404

from core.utils import prepare_data
from rooms.models import Room


def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    heating_data = room.d_heating.heating_data
    lighting_data = room.d_lighting.lighting_data

    # Prepare data (today) for chart
    chart_data_1, chart_data_1_threshold = prepare_data(heating_data,
                                                        "temperature_inside",
                                                        "temperature_outside")
    chart_data_2, chart_data_2_threshold = prepare_data(lighting_data,
                                                        "brightness_inside",
                                                        "brightness_outside")

    context = {
        "room": room,
        "temperature_outside": heating_data.last().temperature_outside,
        "temperature_inside": heating_data.last().temperature_inside,
        "brightness_outside": lighting_data.last().brightness_outside / 2.5,
        "brightness_inside": lighting_data.last().brightness_inside / 2.5,
        "chart_data_1": chart_data_1,
        "chart_data_1_threshold": chart_data_1_threshold,
        "chart_data_2": chart_data_2,
        "chart_data_2_threshold": chart_data_2_threshold,
    }

    return render(request, 'rooms/room.html', context=context)
