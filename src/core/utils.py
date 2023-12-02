import requests
from datetime import date, datetime
import ephem

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


# Machine Learning
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


def prepare_data_heating(instance):
    """Prepares data heating for prediction

    Parameters
    ----------
    instance (HeatingData): an instance of heating device data

    Return
    ------
    a list of data converted into digital form for the model (list)
    """
    season = {"printemps": 0, "été": 1, "automne": 2, "hiver": 3}
    weather = get_weather_data()
    cloudcover = int(weather["current"]["cloudcover"] < 40)  # convert percent cloud cover to binary

    transform_data = [
        0,  # mode night/day
        get_state_sun(weather),  # naturel day or night (sun)
        cloudcover,  # cloud cover (clear or covered)
        season[get_season_now()],  # season
        instance.temperature_outside  # temperature outside
    ]

    return transform_data


def run_model_heating(instance):
    """Load and make a prediction with the Heating model

    Parameters
    ----------
    instance (HeatingData): an instance of heating device data

    Return
    ------
    prediction of the ideal room temperature by the machine learning model (int)
    """
    # load model
    model = load_model("model_heating.pkl")

    # make a prediction
    poly = PolynomialFeatures(degree=2)
    print(prepare_data_heating(instance))
    sample_data_poly = poly.fit_transform([prepare_data_heating(instance)])
    prediction = round(model.predict(sample_data_poly)[0])

    return prediction
