from django.shortcuts import render

from consumption.utils import prepare_data_consumption_lighting, prepare_data_consumption_home_appliance, \
    prepare_data_consumption_heating, prepare_data_heating_price
from rooms.models import Room
from consumption.models import HeatingPrices


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
    all_prices = HeatingPrices.objects.all()
    heating_datas = prepare_data_consumption_heating(all_rooms)
    heating_prices = prepare_data_heating_price(all_prices)

    context = {"heating_data": heating_datas, "heating_prices": heating_prices}

    return render(request, 'consumption/heating.html', context=context)
