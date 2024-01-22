from datetime import date, datetime
import requests
import ephem


def get_weather_data(city="Namur"):
    """Retrieves current weather data for a given city

    Parameters
    ----------
    city (str): Name of the city for which you wish to obtain weather data.

    Returns:
        weather_data (dict): Current weather data in JSON format.
    """
    key = "1829795ae6104bacae16af824bb87c5e"  # Pas bonne pratique

    url = f"http://api.weatherstack.com/current?access_key={key}&query={city}"

    # Send HTTP GET request to URL and convert JSON response into a dictionary
    weather_data = requests.get(url).json()

    if "error" in weather_data:
        print("Expired key !!!!")
        # Json type au cas où la clé de l'API expire
        weather_data = {'request': {'type': 'City', 'query': 'Namur, Belgium', 'language': 'en', 'unit': 'm'},
                             'location': {'name': 'Namur', 'country': 'Belgium', 'region': '', 'lat': '50.467', 'lon': '4.867', 'timezone_id': 'Europe/Brussels', 'localtime': '2024-01-22 16:40', 'localtime_epoch': 1705941600, 'utc_offset': '1.0'},
                             'current': {'observation_time': '03:40 PM', 'temperature': 9, 'weather_code': 116, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png'], 'weather_descriptions': ['Partly cloudy'], 'wind_speed': 33, 'wind_degree': 250, 'wind_dir': 'WSW', 'pressure': 1013, 'precip': 0, 'humidity': 66, 'cloudcover': 75, 'feelslike': 5, 'uv_index': 2, 'visibility': 10, 'is_day': 'yes'}
                             }
    
    return weather_data


def get_season_now():
    """Get the current season based on the current date.

    Returns
    -------
    season (str): A string representing the current season ("spring", "summer", "autumn", or "winter")

    """
    now = date.today()
    month_day = (now.month, now.day)

    if (3, 21) <= month_day < (6, 21):
        season = "printemps"
    elif (6, 21) <= month_day < (9, 21):
        season = "été"
    elif (9, 21) <= month_day < (12, 21):
        season = "automne"
    else:
        season = "hiver"

    return season


def get_state_sun(weather):
    # get location with weather API
    weather_location = weather["location"]

    # create observer with geographic coordinates
    observateur = ephem.Observer()
    observateur.lat = weather_location["lat"]
    observateur.lon = weather_location["lon"]

    observateur.date = datetime.today()

    sunrise = observateur.next_rising(ephem.Sun())
    sunset = observateur.next_setting(ephem.Sun())

    return 1 if sunrise < observateur.date < sunset else 0
