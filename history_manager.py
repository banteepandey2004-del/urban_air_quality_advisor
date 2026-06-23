import csv
import json
from pathlib import Path

from models import AirQualityRecord


class HistoryManager:

    def __init__(self, filename="data/search_history.json"):
        self.filename = Path(filename)
        self.records = []
        self.load_history()

    def load_history(self):
        try:
            if not self.filename.exists():
                self.records = []
                return

            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.records = [
                    AirQualityRecord.from_dict(item) for item in data
                ]

        except json.JSONDecodeError:
            print("History file is corrupted. Starting with empty history.")
            self.records = []

        except OSError as error:
            print(f"File loading error: {error}")
            self.records = []

    def save_history(self):
        try:
            self.filename.parent.mkdir(parents=True, exist_ok=True)

            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(
                    [record.to_dict() for record in self.records],
                    file,
                    indent=4,
                )

        except OSError as error:
            print(f"File saving error: {error}")

    def add_record(self, record):
        self.records.append(record)
        self.save_history()

    def get_all_records(self):
        return self.records

    def export_to_csv(self, filename="exports/air_quality_report.csv"):
        if not self.records:
            print("No records available to export.")
            return

        export_path = Path(filename)

        try:
            export_path.parent.mkdir(parents=True, exist_ok=True)

            with open(export_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "City",
                    "Country",
                    "Time",
                    "PM2.5",
                    "PM10",
                    "Carbon Monoxide",
                    "Nitrogen Dioxide",
                    "Sulphur Dioxide",
                    "Ozone",
                    "UV Index",
                    "Risk Level",
                    "Recommendation",
                ])

                for record in self.records:
                    writer.writerow([
                        record.city,
                        record.country,
                        record.time,
                        record.pm25,
                        record.pm10,
                        record.carbon_monoxide,
                        record.nitrogen_dioxide,
                        record.sulphur_dioxide,
                        record.ozone,
                        record.uv_index,
                        record.risk_level,
                        record.recommendation,
                    ])

            print(f"CSV exported successfully: {export_path}")

        except OSError as error:
            print(f"CSV export error: {error}")
    
    def filter_by_city(self, city_name):
        city_name = city_name.strip().lower()

        return [
            record for record in self.records
            if record.city.lower() == city_name
        ]

    def filter_by_risk_level(self, risk_level):
        risk_level = risk_level.strip().lower()

        return [
            record for record in self.records
            if record.risk_level.lower() == risk_level
        ]