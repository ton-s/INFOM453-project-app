import requests


def get_weather_data(city:str ="Namur"):
    """Retrieves current weather data for a given city

    Parameters
    ----------
    city (str): Name of the city for which you wish to obtain weather data.

    Returns:
        weather_data (dict): Current weather data in JSON format.
    """
    key = "3448cb1dd62b9758038f490877c25fb6"  # Pas bonne pratique

    url = f"http://api.weatherstack.com/current?access_key={key}&query={city}"

    # Send HTTP GET request to URL and convert JSON response into a dictionary
    weather_data = requests.get(url).json()

    return weather_data
