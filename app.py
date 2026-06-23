from api_client import AirQualityClient, GeoCodingClient
from history_manager import HistoryManager
from risk_analyzer import RiskAnalyzer
from validators import is_valid_city_name, is_valid_menu_choice
from input_file_reader import CityFileReader

class AirQualityApp:

    def __init__(self):
        self.geocoding_client = GeoCodingClient()
        self.air_quality_client = AirQualityClient()
        self.history_manager = HistoryManager()

    def run(self):
        while True:
            self.show_menu()
            choice = input("Choose an option: ").strip()

            if not is_valid_menu_choice(choice, {"1", "2", "3", "4", "5","6","0"}):
                print("Invalid choice. Please try again.")
                continue

            if choice == "1":
                self.search_city_air_quality()
            elif choice == "2":
                self.view_search_history()
            elif choice == "3":
                self.history_manager.export_to_csv()
            elif choice == "4":
                self.filter_history_by_city()
            elif choice == "5":
                self.filter_history_by_risk()
            elif choice == "6":
                self.process_cities_from_file()
            elif choice == "0":
                print("Goodbye.")
                break

    def show_menu(self):
        print("\n--- Urban Air Quality Risk Advisor ---")
        print("1. Search city air quality")
        print("2. View saved search history")
        print("3. Export search history to CSV")
        print("4. Filter history by city")
        print("5. Filter history by risk level")
        print("6. Process cities from input file")
        print("0. Exit")

    def search_city_air_quality(self):
        city_name = input("Enter city name: ").strip()

        if not is_valid_city_name(city_name):
            print(
                "Invalid city name. Use letters, spaces, hyphens, "
                "apostrophes, or dots only."
            )
            return

        analyzed_record = self.get_analyzed_record_for_city(city_name)

        if analyzed_record is None:
            return

        self.display_record(analyzed_record)

        save_choice = input("\nSave this result? yes/no: ").strip().lower()

        if save_choice == "yes":
            self.history_manager.add_record(analyzed_record)
            print("Result saved successfully.")
        else:
            print("Result not saved.")

    def view_search_history(self):
        records = self.history_manager.get_all_records()

        if not records:
            print("No saved search history.")
            return

        print("\n--- Saved Search History ---")

        for index, record in enumerate(records, start=1):
            print(f"\nRecord {index}")
            self.display_record(record)

    @staticmethod
    def display_record(record):
        print("\n--- Air Quality Result ---")
        print(f"Location: {record.city}, {record.country}")
        print(f"Time: {record.time}")
        print(f"PM2.5: {record.pm25}")
        print(f"PM10: {record.pm10}")
        print(f"Carbon monoxide: {record.carbon_monoxide}")
        print(f"Nitrogen dioxide: {record.nitrogen_dioxide}")
        print(f"Sulphur dioxide: {record.sulphur_dioxide}")
        print(f"Ozone: {record.ozone}")
        print(f"UV index: {record.uv_index}")

        print("\n--- Risk Assessment ---")
        print(f"Risk level: {record.risk_level}")
        print(f"Recommendation: {record.recommendation}")
    
    def filter_history_by_city(self):
        city_name = input("Enter city name to filter: ").strip()

        if not is_valid_city_name(city_name):
            print(
                "Invalid city name. Use letters, spaces, hyphens, "
                "apostrophes, or dots only."
            )
            return

        results = self.history_manager.filter_by_city(city_name)

        if not results:
            print("No saved records found for this city.")
            return

        print(f"\n--- Records for {city_name} ---")

        for record in results:
            self.display_record(record)

    def filter_history_by_risk(self):
        risk_level = input(
            "Enter risk level: Low, Moderate, High, Very High, or Unknown: "
        ).strip()

        valid_risks = {"low", "moderate", "high", "very high", "unknown"}

        if risk_level.lower() not in valid_risks:
            print("Invalid risk level.")
            return

        results = self.history_manager.filter_by_risk_level(risk_level)

        if not results:
            print("No saved records found for this risk level.")
            return

        print(f"\n--- Records with {risk_level} risk ---")

        for record in results:
            self.display_record(record)
    
    def get_analyzed_record_for_city(self, city_name):
        locations = self.geocoding_client.search_city(city_name)

        if not locations:
            print(f"No matching city found for: {city_name}")
            return None

        location = locations[0]

        record = self.air_quality_client.fetch_air_quality(location)

        if record is None:
            print(f"No air-quality data found for: {city_name}")
            return None

        return RiskAnalyzer.classify(record)
    
    def process_cities_from_file(self):
        filename = input(
            "Enter input file path, for example inputs/cities.txt: "
        ).strip()

        reader = CityFileReader(filename)
        city_names, invalid_lines = reader.read_city_names()

        if invalid_lines:
            print("\nInvalid lines skipped:")

            for line_number, city_name in invalid_lines:
                print(f"Line {line_number}: {city_name}")

        if not city_names:
            print("No valid city names found in the input file.")
            return

        success_count = 0
        failed_count = 0

        for city_name in city_names:
            print(f"\nProcessing city: {city_name}")

            analyzed_record = self.get_analyzed_record_for_city(city_name)

            if analyzed_record is None:
                failed_count += 1
                continue

            self.display_record(analyzed_record)
            self.history_manager.add_record(analyzed_record)
            success_count += 1

        print("\n--- Batch Processing Summary ---")
        print(f"Successful records saved: {success_count}")
        print(f"Failed city searches: {failed_count}")
        print(f"Invalid input lines skipped: {len(invalid_lines)}")