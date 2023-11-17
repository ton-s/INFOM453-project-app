from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from rooms.utils import prepare_data
from rooms.models import Room, LightingData, Notification


def room(request, slug):
    """Revoir le calcule de la luminosté extérieur (lux) et intérieur (lumen) et revoir graphique !!!"""

    room = get_object_or_404(Room, slug=slug)
    device_heating = room.d_heating
    device_lighting = room.d_lighting
    heating_data = device_heating.heating_data
    lighting_data = device_lighting.lighting_data

    if heating_data.exists() and lighting_data.exists():

        # Check notification
        notif_heating = device_heating.heating_notifications.last()
        if notif_heating:
            messages.info(request, f"{notif_heating.content} ({notif_heating.timestamp.strftime('%H:%M')})",
                          extra_tags="Chauffage")

        notif_ligthing = device_lighting.lighting_notifications.last()
        if notif_ligthing:
            messages.info(request, f"{notif_ligthing.content} ({notif_ligthing.timestamp.strftime('%H:%M')})",
                          extra_tags="Éclairage")

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
            "brightness_outside": lighting_data.last().get_type_brightness(),
            "brightness_inside": LightingData.convert_lumen_to_percent(lighting_data.last().brightness_inside),
            "chart_data_1": chart_data_1,
            "chart_data_1_threshold": chart_data_1_threshold,
            "chart_data_2": chart_data_2,
            "chart_data_2_threshold": chart_data_2_threshold,
        }

        return render(request, 'rooms/room.html', context=context)

    else:
        # Indicates that the request is not allowed
        return HttpResponseBadRequest("Pas de données disponibles")


def increase_temperature(request, slug):
    if request.method == "POST":
        room = get_object_or_404(Room, slug=slug)
        last_data = room.d_heating.heating_data.last()
        new_temp_desired = int(last_data.increase())

        return HttpResponse(f"{new_temp_desired}°C")

    else:
        # Indicates that the request is not allowed
        return HttpResponseBadRequest("Méthode non autorisée")


def decrease_temperature(request, slug):
    if request.method == "POST":
        room = get_object_or_404(Room, slug=slug)
        last_data = room.d_heating.heating_data.last()
        new_temp_desired = int(last_data.decrease())

        return HttpResponse(f"{new_temp_desired}°C")

    else:
        # Indicates that the request is not allowed
        return HttpResponseBadRequest("Méthode non autorisée")


def change_brightness(request, slug):
    if request.method == "POST":
        data = int(request.POST.get("light-range"))
        data_lumen = LightingData.convert_percent_to_lum(data)
        room = get_object_or_404(Room, slug=slug)
        last_data = room.d_lighting.lighting_data.last()
        new_brightness_desired = last_data.change_brightness(data_lumen)

        return HttpResponse(f"{LightingData.convert_lumen_to_percent(new_brightness_desired)}%")

    else:
        # Indicates that the request is not allowed
        return HttpResponseBadRequest("Méthode non autorisée")


def notification_valid(request, slug, type):
    if request.method == "POST":
        room = get_object_or_404(Room, slug=slug)

        if type == "chauffage":
            notif = room.d_heating.heating_notifications.first()
            data = room.d_heating.heating_data.last()
            data.set_temperature_desired(notif.action)

        else:
            notif = room.d_lighting.lighting_notifications.first()
            data = room.d_lighting.lighting_data.last()
            data.set_brightness_desired(notif.action)


        if notif:
            notif.delete()
            return HttpResponse(status=200)
        else:
            return HttpResponseBadRequest("Notification non trouvée")

    else:
        # Indicates that the request is not allowed
        return HttpResponseBadRequest("Méthode non autorisée")


def notification_close(request, slug, type):
    if request.method == "POST":
        room = get_object_or_404(Room, slug=slug)

        if type == "chauffage":
            notif = room.d_heating.heating_notifications.first()
        else:
            notif = room.d_lighting.lighting_notifications.first()

        if notif:
            notif.delete()
            return HttpResponse(status=200)
        else:
            return HttpResponseBadRequest("Notification non trouvée")

    else:
        # Indicates that the request is not allowed
        return HttpResponseBadRequest("Méthode non autorisée")



