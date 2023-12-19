from django.shortcuts import render

from consumption.utils import prepare_data_consumption_lighting, prepare_data_consumption_home_appliance, \
    heating_consumption_calculator, prepare_data_consumption_heating
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
   
    all_rooms = Room.objects.all()
    heating_datas = prepare_data_consumption_heating(all_rooms)
   
    print(heating_datas)
    colors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
        "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
        "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173",
        "#5254a3", "#637939", "#8c6d31", "#843c39", "#7b4173",
    ]
    context = {"heating_data": heating_datas, "colors": colors}

    return render(request, 'consumption/heating.html', context=context)
