# Urban Air Quality Risk Advisor

A Python command-line application that helps users check urban air-quality risk before outdoor activities such as walking, cycling, running, commuting, or working outside.

The application searches for a city, retrieves air-quality pollutant values from external APIs, classifies the result into a risk level, and provides a simple outdoor activity recommendation.

## Project Overview

This project was developed for the M602 Computer Programming individual project. It demonstrates:

- Python 3 programming
- Object-oriented programming
- Functions and modular code structure
- API integration
- JSON, CSV, and TXT file handling
- Exception handling
- Regular expression validation
- Command-line user interaction
- Git/GitHub version control

## Features

- Search air quality by city name
- Convert city names into latitude and longitude using a geocoding API
- Fetch air-quality data using the Open-Meteo Air Quality API
- Display pollutant values:
  - PM2.5
  - PM10
  - Carbon monoxide
  - Nitrogen dioxide
  - Sulphur dioxide
  - Ozone
  - UV index
- Classify air-quality risk as:
  - Low
  - Moderate
  - High
  - Very High
  - Unknown
- Provide outdoor activity recommendations
- Save search history to a JSON file
- View saved search history
- Filter saved records by city
- Filter saved records by risk level
- Export saved records to CSV
- Process multiple cities from a TXT file
- Validate city names using regular expressions
- Handle API, file, and input errors safely

## APIs Used

This project uses Open-Meteo APIs:

- Open-Meteo Geocoding API  
  https://open-meteo.com/en/docs/geocoding-api

- Open-Meteo Air Quality API  
  https://open-meteo.com/en/docs/air-quality-api

The geocoding API converts a city name into latitude and longitude. The air-quality API uses those coordinates to retrieve pollutant values.

## Project Structure

```text
urban_air_quality_advisor/
├── main.py
├── app.py
├── models.py
├── api_client.py
├── risk_analyzer.py
├── validators.py
├── history_manager.py
├── input_file_reader.py
├── data/
│   └── search_history.json
├── inputs/
│   └── cities.txt
├── exports/
│   └── air_quality_report.csv
├── requirements.txt
├── README.md
└── .gitignore
```

## File Descriptions

| File | Description |
|---|---|
| `main.py` | Starts the application. |
| `app.py` | Controls the command-line menu and user workflow. |
| `models.py` | Contains the `Location` and `AirQualityRecord` data classes. |
| `api_client.py` | Handles geocoding and air-quality API requests. |
| `risk_analyzer.py` | Classifies pollutant values into risk levels. |
| `validators.py` | Validates city names and menu choices. |
| `history_manager.py` | Saves, loads, filters, and exports search history. |
| `input_file_reader.py` | Reads and validates city names from a text file. |
| `data/search_history.json` | Stores saved search history. |
| `inputs/cities.txt` | Stores city names for batch processing. |
| `exports/air_quality_report.csv` | Stores exported CSV results. |

## Requirements

- Python 3.10 or above
- Internet connection
- `requests` library

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git
cd YOUR-REPOSITORY-NAME
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not created yet, install the required package manually:

```bash
pip install requests
```

## How to Run

Run the application from the project folder:

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

## Menu Options

When the program starts, the user can choose from the following options:

```text
1. Search city air quality
2. View saved search history
3. Export search history to CSV
4. Filter history by city
5. Filter history by risk level
6. Process cities from input file
0. Exit
```

## Example Usage

### Search for a City

```text
Enter your choice: 1
Enter city name: Berlin
```

Example output:

```text
Location: Berlin, Germany
PM2.5: 3.7
PM10: 5.4
Carbon monoxide: 147.0
Nitrogen dioxide: 7.2
Sulphur dioxide: 1.0
Ozone: 68.0
UV index: 0.0
Risk level: Moderate
Recommendation: Outdoor activity is acceptable, but sensitive users should reduce prolonged exposure.
```

The actual values may change because the application retrieves live API data.

## Batch Input File

To process multiple cities, create or edit:

```text
inputs/cities.txt
```

Example content:

```text
Berlin
Delhi
London
@@@
Paris
```

Run the application and choose option `6`.

The program will process valid city names and skip invalid lines.

## Output Files

### JSON Search History

Saved records are stored in:

```text
data/search_history.json
```

This file keeps previous searches after the program closes.

### CSV Export

Exported records are stored in:

```text
exports/air_quality_report.csv
```

This file can be opened in Excel, Google Sheets, or other spreadsheet software.

## Error Handling

The application handles:

- Invalid city names
- Invalid menu choices
- No matching city found
- API timeout errors
- Network connection errors
- HTTP errors
- Invalid JSON responses
- Missing input files
- Corrupted JSON history files
- CSV export errors
- Keyboard interruption

## Limitations

- The application requires an internet connection.
- Results depend on API availability and response quality.
- Some pollutant values may be missing from the API response.
- The risk classification is simplified and should not be used as medical or professional environmental advice.
- If multiple cities share the same name, the application currently uses the first matching API result.

## Future Improvements

Possible future improvements include:

- Letting the user choose from multiple city search results
- Adding pollutant trend charts
- Calculating 24-hour averages
- Comparing air quality between two cities
- Adding a graphical user interface
- Adding official regional AQI threshold options
- Adding automated tests

## Author

Bantee Pandey

M602 Computer Programming  
Gisma University of Applied Sciences

## Disclaimer

This project is an educational programming project. The recommendations are simplified and should not be treated as professional medical, environmental, or health advice.
