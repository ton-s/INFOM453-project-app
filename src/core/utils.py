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
