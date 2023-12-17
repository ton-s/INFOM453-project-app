from django.shortcuts import render

from consumption.utils import prepare_data_consumption_lighting, prepare_data_consumption_home_appliance, \
    heating_consumption_calculator
from rooms.models import Room


def electric_consumption(request):
    # electric global
    global_lighting_chart_data = prepare_data_consumption_lighting(0, 9)
    global_lighting_chart_data_threshold = prepare_data_consumption_lighting(8, 10)

    context = {
        'global_lighting_chart_data': global_lighting_chart_data,
        'global_lighting_chart_data_threshold': global_lighting_chart_data_threshold,
        'home_appliance_chart_data': prepare_data_consumption_home_appliance(),
    }

    return render(request, 'consumption/electric.html', context=context)


def heating_consumption(request):
    heating_consumption = 0
    rooms_heating_datas = {}
    all_rooms = Room.objects.all()
    if all_rooms.exists():
        for room in all_rooms:
            heating_datas = room.d_heating.heating_data.all()
            if heating_datas.exists():
                rooms_heating_datas[room.name] = []
                for heating_data in heating_datas:
                    temperature_inside = heating_data.temperature_inside
                    temperature_targeted = heating_data.temperature_desired
                    starting_time = heating_data.timestamp
                    room_volume = 30 * 2.5  # room surface * room height
                    heating_type = 'oil'
                    heating_consumption = heating_consumption_calculator(heating_type, temperature_inside,
                                                                         temperature_targeted, room_volume,
                                                                         starting_time)

                    rooms_heating_datas[room.name].append(
                        {'x': int(starting_time.timestamp()) * 1000, 'y': heating_consumption})

    colors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
        "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
        "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173",
        "#5254a3", "#637939", "#8c6d31", "#843c39", "#7b4173",
    ]
    context = {"heating_data": rooms_heating_datas, "colors": colors}

    return render(request, 'consumption/heating.html', context=context)
