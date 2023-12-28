import datetime
import random
import requests
from consumption.models import HeatingPrices
from bs4 import BeautifulSoup

from rooms.models import HomeAppliance

def prepare_data_consumption_heating(rooms):
    heating_consumption = 0
    consumptionByMonth = {"Jan": 250, "Feb": 224, "Mar": 203, "Apr": 180, "May": 132, "Jun": 90, "Jul": 69, "Aug": 74, "Sep": 120,
                            "Oct": 197, "Nov": 224, "Dec": 238}
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
    print(data_points)
    
    return data_points

def setTimestampToMonth(timestamp):
    #cast timestamp to datetime object
    month = datetime.datetime.fromtimestamp(timestamp.timestamp()).strftime('%b')
    return month

def prepare_data_heating_price(prices):
    get_today_data = True
    all_dates = ["2023-12-21","2023-12-14","2023-12-07","2023-11-30","2023-11-23","2023-11-16","2023-11-09","2023-11-02","2023-10-26","2023-10-19","2023-10-12","2023-10-05","2023-09-28","2023-09-21","2023-09-14","2023-09-07"]
    all_prices = ["0.91860","0.87820","0.93600","0.97140","0.96460","0.98520","1.00730","1.01590","1.02530","1.05890","1.04030","1.08120","1.08340","1.09890","1.11860","1.07120"]
    if prices.exists():
        all_dates.reverse()
        all_prices.reverse()
        get_today_data = False
        for thisprice in prices : 
            all_prices.append(float(thisprice.price))
            all_dates.append(str(thisprice.date))
            #if thisprice.date is older than 7 days, get_today_data = true
            if thisprice.date < datetime.date.today() - datetime.timedelta(days=7):
                get_today_data = True
    
    if get_today_data:
        url = "https://petrolprices.economie.fgov.be/petrolprices/?locale=fr"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            data_element = soup.find('tr', {'class': 'ui-widget-content ui-datatable-odd second-row', 'data-ri':"3"})
            data_element = data_element.find('td', {'role': 'gridcell', "style": "text-align: center;width:25%;border:none!important;"}).get_text(strip=True)
            new_price = data_element.replace(",", ".")
            new_price = ''.join(c for c in new_price if c.isdigit() or c in {'.', ','})
            today_date = datetime.date.today()
            all_prices.append(new_price)
            all_dates.append(today_date)
            new_entry = HeatingPrices(date=today_date, price=new_price)
            new_entry.save()
        else :
            print("error")

    data_points = [{"label": str(date), "y": float(price)} for date,price in zip(all_dates,all_prices)]
    print(data_points)
    
    return data_points

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
    consumption = (heating_power_needed * heating_time) / mean_lower_heating_volume  # in L

    return consumption
