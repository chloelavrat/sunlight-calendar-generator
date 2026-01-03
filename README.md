<div align="center">
  <img src="./assets/README-banner.png" alt="Banner" style="border-radius: 17px; width: 100%; max-width: 800px; height: auto;">
</div>

<h3 align="center">
  <b><a href="azerty-labs.com">Online App</a></b>
  •
  <b><a href="#usage">Usage</a></b>
  •
  <b><a href="https://github.com/chloelavrat/sunlight-calendar-generator/blob/main/assets/banner.png">App Screenshot</a></b>
</h3>

<div align="center">
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python Versions">
</div>
</br>

<p align="center">
  The <b>Sunlight Calendar Generator</b> is a Streamlit application that generates iCal calendar files with daily sunrise, sunset, and daylight duration information for any location worldwide. The app leverages the <a href="https://github.com/sffjunkie/astral">astral</a> library to calculate precise astronomical data, perfect for photographers, travelers, and anyone optimizing their schedule around sunlight.
</p>

## Features

The Sunlight Calendar Generator offers the following features:

- **Generate Daylight Calendars:** Create iCal calendar files with daily sunrise, sunset, and daylight duration for any location worldwide.
- **Location Selection:** Choose from hundreds of pre-configured cities or use custom coordinates.
- **Flexible Date Ranges:** Select any start and end date for your calendar.
- **Timezone Support:** Full timezone support with UTC offset display.
- **Polar Night/Midnight Sun Handling:** Automatically handles extreme latitude locations with polar night or midnight sun conditions.

## How it Works

The app uses the `astral` library to calculate precise sunrise and sunset times based on geographic coordinates. It generates iCal (`.ics`) calendar files that can be imported into any calendar application (Google Calendar, Apple Calendar, Outlook, etc.).

When you select a location and date range, the app:
1. Calculates sunrise and sunset times for each day in the range
2. Computes the daylight duration
3. Creates calendar events with detailed information
4. Generates a downloadable iCal file

The calendar events include:
- Sunrise and sunset times
- Daylight duration in hours and minutes
- Location coordinates and timezone information
- Special handling for polar night/midnight sun days

## Run app locally

If you want to run the **sunlight-calendar-generator** streamlit app locally. Multiple solutions are possible:

1. **Run the app directly in a virtual environment**
    
    Clone repository:
    ```
    git clone https://github.com/chloelavrat/sunlight-calendar-generator.git
    cd sunlight-calendar-generator
    ```
    Create, activate and install your environment:
    ```
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
    Run the app using streamlit:
    ```
    streamlit run streamlit_app.py
    ```

2. **Run the app using docker**

    Build the `sunlight-calendar-generator` docker container:
    ```
    docker build -t sunlight-calendar-generator .
    ```
    Run the container at a specified port (here 8501) 
    ```
    docker run -p 8501:8501 sunlight-calendar-generator
    ```
    Go to your web browser and access [localhost:8501](http://localhost:8501)

## Contributing

This is an open-source project, and contributions are always welcome. If you would like to contribute to the project, you can do so by submitting a pull request or by creating an issue on the project's GitHub page.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
