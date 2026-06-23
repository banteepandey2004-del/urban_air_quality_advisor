from pathlib import Path

from validators import is_valid_city_name


class CityFileReader:

    def __init__(self, filename):
        self.filename = Path(filename)

    def read_city_names(self):
        valid_cities = []
        invalid_lines = []

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    city_name = line.strip()

                    if not city_name:
                        continue

                    if is_valid_city_name(city_name):
                        valid_cities.append(city_name)
                    else:
                        invalid_lines.append((line_number, city_name))

        except FileNotFoundError:
            print(f"Input file not found: {self.filename}")
            return [], []

        except OSError as error:
            print(f"File reading error: {error}")
            return [], []

        return valid_cities, invalid_lines