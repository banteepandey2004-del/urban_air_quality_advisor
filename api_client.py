import requests

from models import AirQualityRecord, Location


class GeoCodingClient:

    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

    def search_city(self, city_name):
        try:
            response = requests.get(
                self.BASE_URL,
                params={
                    "name": city_name,
                    "count": 5,
                    "language": "en",
                    "format": "json",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

        except requests.exceptions.Timeout:
            print("Geocoding API timed out. Please try again later.")
            return []

        except requests.exceptions.ConnectionError:
            print("Network error. Please check your internet connection.")
            return []

        except requests.exceptions.HTTPError as error:
            print(f"Geocoding HTTP error: {error}")
            return []

        except requests.exceptions.RequestException as error:
            print(f"Geocoding API error: {error}")
            return []

        except ValueError:
            print("Invalid JSON response from geocoding API.")
            return []

        return self._parse_locations(data)

    def _parse_locations(self, data):
        results = data.get("results", [])

        if not results:
            return []

        locations = []

        for item in results:
            latitude = item.get("latitude")
            longitude = item.get("longitude")

            if latitude is None or longitude is None:
                continue

            locations.append(
                Location(
                    city=item.get("name", "Unknown"),
                    country=item.get("country", "Unknown"),
                    latitude=latitude,
                    longitude=longitude,
                    timezone=item.get("timezone", ""),
                )
            )

        return locations


class AirQualityClient:

    BASE_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

    def fetch_air_quality(self, location):
        try:
            response = requests.get(
                self.BASE_URL,
                params={
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "hourly": (
                        "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,"
                        "sulphur_dioxide,ozone,uv_index"
                    ),
                    "forecast_days": 1,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

        except requests.exceptions.Timeout:
            print("Air-quality API timed out. Please try again later.")
            return None

        except requests.exceptions.ConnectionError:
            print("Network error. Please check your internet connection.")
            return None

        except requests.exceptions.HTTPError as error:
            print(f"Air-quality HTTP error: {error}")
            return None

        except requests.exceptions.RequestException as error:
            print(f"Air-quality API error: {error}")
            return None

        except ValueError:
            print("Invalid JSON response from air-quality API.")
            return None

        return self._parse_latest_record(data, location)

    def _parse_latest_record(self, data, location):
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])

        if not hourly or not times:
            print("Air-quality response does not contain hourly data.")
            return None

        index = 0

        return AirQualityRecord(
            city=location.city,
            country=location.country,
            time=times[index],
            pm25=self._get_value(hourly, "pm2_5", index),
            pm10=self._get_value(hourly, "pm10", index),
            carbon_monoxide=self._get_value(hourly, "carbon_monoxide", index),
            nitrogen_dioxide=self._get_value(hourly, "nitrogen_dioxide", index),
            sulphur_dioxide=self._get_value(hourly, "sulphur_dioxide", index),
            ozone=self._get_value(hourly, "ozone", index),
            uv_index=self._get_value(hourly, "uv_index", index),
        )

    @staticmethod
    def _get_value(hourly, key, index):
        values = hourly.get(key, [])

        if not values or index >= len(values):
            return None

        return values[index]