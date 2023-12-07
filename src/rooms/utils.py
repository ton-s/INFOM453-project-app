from django.utils import timezone
import random
import pickle
import json
from sklearn.preprocessing import PolynomialFeatures

from core.utils import get_weather_data, get_season_now, get_state_sun
from thermo.settings import BASE_DIR
from rooms.models import LightingData


def prepare_data(data, inside, outside):
    """Prepares data for a graph by extracting the necessary information

    Parameters
    ----------
    - data: QuerySet (ex: heating_data or heating_data)
    - inside (str): Character string representing the name of the data field inside (ex: "temperature_inside").
    - outside (str): Character string representing the name of the data field outside (ex: "temperature_outside")
    - y_pourcent
    Returns
    -------
    - chart_data (list of dict): data inside, with the key 'x' (timestamp) et 'y' (value inside)
    - chart_data_threshold (list of dict): data outside, with the key 'x' (timestamp) et 'y' (value outside)
    """
    today = timezone.now().date()
    chart_data = []
    chart_data_threshold = []

    for entry in data.filter(timestamp__date=today):
        timestamp_ms = int(entry.timestamp.timestamp()) * 1000  # Format Unix

        # get data from the database
        value_inside = int(getattr(entry, inside))
        value_outside = int(getattr(entry, outside))

        if inside == "brightness_inside" and outside == "brightness_outside":
            value_inside = LightingData.convert_lumen_to_percent(value_inside)
            value_outside = LightingData.convert_lux_to_percent(value_outside)

        chart_data.append({"x": timestamp_ms, "y": value_inside})
        chart_data_threshold.append({"x": timestamp_ms, "y": value_outside})

    return chart_data, chart_data_threshold


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

    # prepare model and data
    poly = PolynomialFeatures(degree=2)
    print(prepare_data_heating(instance))
    prepared_data = prepare_data_heating(instance)
    sample_data_poly = poly.fit_transform([prepared_data])

    # make a prediction
    prediction = round(model.predict(sample_data_poly)[0])

    return prediction


def run_model_lighting(instance):
    """Load and make a prediction with the Lighting model

    Parameters
    ----------
    instance (LightingData): an instance of lighting device data

    Return
    ------
    prediction of ideal brightness by machine learning model (int)
    """
    # load model
    model = load_model("model_lighting.pkl")

    # prepare data
    prepared_data = [get_state_sun(get_weather_data()), instance.brightness_outside]

    # make a prediction
    prediction = model.predict([prepared_data])[0]

    return prediction


# notification
def load_json(file):
    path = BASE_DIR / 'static/json/' / file
    with open(path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    return data


def get_notification(value, too):
    """Generate a random notification

    Parameters
    ----------
    value (int) : ideal value
    too (str) : notification type

    Return
    ------
    notification (str) : random notification of value justification
    """
    # load json
    data = load_json("notifications.json")

    # generate random notification
    random_notification = random.choice(data[too]["justifications"])
    notification = random_notification.replace("{{value}}", str(value))

    return notification
