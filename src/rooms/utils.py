from django.utils import timezone

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
