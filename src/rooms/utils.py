from django.utils import timezone


def prepare_data(data, inside, outside):
    """Prepares data for a graph by extracting the necessary information

    Parameters
    ----------
    - data: QuerySet (ex: heating_data or heating_data)
    - inside (str): Character string representing the name of the data field inside (ex: "temperature_inside").
    - outside (str): Character string representing the name of the data field outside (ex: "temperature_outside")
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
        chart_data.append({"x": timestamp_ms, "y": int(getattr(entry, inside))})
        chart_data_threshold.append({"x": timestamp_ms, "y": int(getattr(entry, outside))})

    return chart_data, chart_data_threshold
