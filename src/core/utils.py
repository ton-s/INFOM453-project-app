import requests
from datetime import date


def get_weather_data(city="Namur"):
    """Retrieves current weather data for a given city

    Parameters
    ----------
    city (str): Name of the city for which you wish to obtain weather data.

    Returns:
        weather_data (dict): Current weather data in JSON format.
    """
    key = "25cd8ec6f4c2c912b8b5bec00cc2795c"  # Pas bonne pratique

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

    Raises
    ------
    IndexError: If the calculated value doesn't match any known season.
    """
    now = date.today()
    month = now.month * 100
    day = now.day
    month_day = month + day  # combining month and day

    if (month_day >= 301) and (month_day <= 531):
        season = "printemps"
    elif (month_day > 531) and (month_day < 901):
        season = "été"
    elif (month_day >= 901) and (month_day <= 1130):
        season = "automne"
    elif (month_day > 1130) and (month_day <= 229):
        season = "hiver"
    else:
        raise IndexError("Invalid")

    return season
