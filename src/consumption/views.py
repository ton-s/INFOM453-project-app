from django.shortcuts import render
from rooms.models import Room
from consumption.utils import heating_consumption_calculator
from datetime import datetime
# Create your views here.

def consumption(request):
    return render(request, 'consumption/consumption.html')

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
                    room_volume = 30*2.5 # room surface * room height
                    heating_type = 'oil'
                    heating_consumption = heating_consumption_calculator(heating_type,temperature_inside,temperature_targeted,room_volume,starting_time)

                    rooms_heating_datas[room.name].append({'x':int(starting_time.timestamp())*1000, 'y':heating_consumption})
                    
    colors = [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
                "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
                "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
                "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173",
                "#5254a3", "#637939", "#8c6d31", "#843c39", "#7b4173",
                ]
    context = {"heating_data": rooms_heating_datas, "colors": colors}
    return render(request, 'consumption/heating.html', context)

def electric_consumption(request):

    home_appliances_datas={}

    #TODO : à opti 
    all_rooms = Room.objects.all()
    if all_rooms.exists():
        for room in all_rooms:
            home_appliances = room.d_homeAppliance.all()
            if home_appliances.exists():
                for home_appliance in home_appliances:
                    home_appliance_datas = home_appliance.homeAppliances_data.all()
                    if home_appliance_datas.exists():
                        home_appliances_datas[home_appliance.name] = []
                        for home_appliance_data in home_appliance_datas:
                            datestamp =int(home_appliance_data.timestamp.timestamp()) * 1000
                            power = home_appliance_data.power
                            home_appliances_datas[home_appliance.name].append({'x':datestamp, 'y':power})
                            
    colors = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
    "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173",
    "#5254a3", "#637939", "#8c6d31", "#843c39", "#7b4173",
]
    context = {"electric_data": home_appliances_datas, "colors": colors}
    return render(request, 'consumption/electric.html', context)