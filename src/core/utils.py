import requests
from datetime import date

import pickle
from sklearn.preprocessing import PolynomialFeatures
from thermo.settings import BASE_DIR


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


def load_model(name_model):
    """Loads a template into the directory named 'ml_models'

    Parameters
    ----------
    name_model (str): the model file

    Returns
    -------
    model (sklearn)
    """
    path = BASE_DIR / f'ml_models/{name_model}'
    with open(path, 'rb') as file:
        model = pickle.load(file)

    return model


def run_model_heating(data):
    """Load and make a prediction with the Heating model

    """
    # load model
    model = load_model("model_heating.pkl")

    # make a prediction
    poly = PolynomialFeatures(degree=2)
    sample_data_poly = poly.fit_transform(data)
    prediction = round(model.predict(sample_data_poly)[0])

    return prediction
