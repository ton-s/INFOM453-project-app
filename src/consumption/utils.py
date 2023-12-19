import datetime
import random

from rooms.models import HomeAppliance

def prepare_data_consumption_heating(rooms):
    heating_consumption = 0
    consumptionByMonth = {"Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0,
                            "Oct": 0, "Nov": 0, "Dec": 0}
    if rooms.exists():
        for room in rooms:
            heating_datas = room.d_heating.heating_data.all()
            if heating_datas.exists():
                for heating_data in heating_datas:
                    temperature_inside = heating_data.temperature_inside
                    temperature_targeted = heating_data.temperature_desired
                    starting_time = heating_data.timestamp
                    month = setTimestampToMonth(starting_time)
                    room_volume = 30 * 2.5  # room surface * room height
                    heating_type = 'oil'
                    heating_consumption = heating_consumption_calculator(heating_type, temperature_inside,
                                                                            temperature_targeted, room_volume,
                                                                            starting_time)
                    consumptionByMonth[month] += heating_consumption
    data_points = [{"label": month, "y": consumption} for month, consumption in consumptionByMonth.items()]
    
    return data_points
def setTimestampToMonth(timestamp):
    #cast timestamp to datetime object
    month = datetime.datetime.fromtimestamp(timestamp.timestamp()).strftime('%b')
    return month

def prepare_data_consumption_lighting(f_a, f_b):
    data = []
    start_date = datetime.date.today().replace(day=1)
    next_month = (start_date.month % 12) + 1
    year = start_date.year + start_date.month // 12

    end_date = datetime.datetime(year, next_month, 1) - datetime.timedelta(days=1)

    current_date = datetime.datetime(start_date.year, start_date.month, 1)

    while current_date <= end_date:
        data_point = {
            'x': int(current_date.timestamp()) * 1000,
            'y': round(random.uniform(f_a, f_b), 2),
        }
        data.append(data_point)
        current_date += datetime.timedelta(days=1)

    return data


def prepare_data_consumption_home_appliance():
    data = {}
    for home_app in HomeAppliance.objects.all():
        data[home_app.name] = []
        for home_app_data in home_app.homeAppliances_data.all():
            data[home_app.name].append({
                'x': int(home_app_data.timestamp.timestamp()) * 1000,
                'y': 0,
                'mode': 'arrêt'
            })

            data[home_app.name].append({
                'x': int(home_app_data.timestamp.timestamp()) * 1000,
                'y': home_app_data.power,
                'mode': home_app_data.mode,
            })
            data[home_app.name].append({
                'x': int(
                    (home_app_data.timestamp + datetime.timedelta(minutes=home_app_data.time_work)).timestamp()) * 1000,
                'y': home_app_data.power,
                'mode': home_app_data.mode,
            })

            data[home_app.name].append({
                'x': int(
                    (home_app_data.timestamp + datetime.timedelta(minutes=home_app_data.time_work)).timestamp()) * 1000,
                'y': 0,
                'mode': 'arrêt'
            })

    return data


def heating_consumption_calculator(heating_type, current_temp, target_temp, room_volume, starting_time):
    # Does not take into account the insulation of the room and the outside temperature
    now = datetime.datetime.now()
    heating_time = now - starting_time
    heating_time = heating_time.total_seconds() / 3600  # in hours

    if heating_type == 'oil':
        mean_lower_heating_volume = 9.96  # in kWh for 1L of oil

    # calculate the power needed to heat the room
    air_volumetric_eat_capacity = 1256  # in J/(m3⋅°C)
    heating_power_needed = (target_temp - current_temp) * air_volumetric_eat_capacity * room_volume  # in J
    heating_power_needed = heating_power_needed / 3600000  # in kilowatts

    # calculate the consumption
    print(heating_time, heating_power_needed)
    consumption = (heating_power_needed * heating_time) / mean_lower_heating_volume  # in L

    return consumption
