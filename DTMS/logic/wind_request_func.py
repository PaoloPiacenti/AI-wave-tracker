import requests
import datetime

def get_wind_info(id_estacao):
    url = "https://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return f"Error accessing API: {e}"

    # Initialize variables to store the most recent data
    l_date = datetime.datetime(2000, 1, 1, 1, 0)
    candidates = []

    #Iterate over the features in the GeoJSON to get all the last observations for the station
    for feature in data.get("features", []):
        properties = feature.get("properties", {})
        if properties.get("idEstacao") == id_estacao:
            candidates.append(properties)

    #Look for the last obeservation
    for c in candidates:
        c_date = datetime.datetime.strptime(c.get("time"), "%Y-%m-%dT%H:%M:%S")
        c_wind = c.get("intensidadeVento")

        if c_date >= l_date:
            l_date = c_date
            if c_wind > 0:
                wind_kn = round(1.944*c_wind)
                wind_dir = str(c.get("descDirVento"))

    return wind_kn, wind_dir
