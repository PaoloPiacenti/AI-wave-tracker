import requests

class WaveForecast:
    def __init__(self, globalIdLocal=1111026):
        self.api_url = "https://api.ipma.pt/open-data/forecast/oceanography/daily/hp-daily-sea-forecast-day0.json"
        self.globalIdLocal = globalIdLocal

    def fetch_data(self):
        response = requests.get(self.api_url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        return response.json()

    def filter_data(self, data):
        if 'data' not in data:
            raise ValueError("Expected key 'data' in response JSON")

        for item in data['data']:
            if item['globalIdLocal'] == self.globalIdLocal:
                return item
        return None

    def run(self):
        try:
            # Fetch data from API
            data = self.fetch_data()

            # Filter data for the specified location
            location_data = self.filter_data(data)

            if location_data:
                # Write data to CSV
                for item in data['data']:
                    if item['globalIdLocal'] == self.globalIdLocal:
                        return item
            else:
                print(f"No data found for {self.globalIdLocal['local']}")
        except Exception as e:
            print(f"An error occurred: {e}")
