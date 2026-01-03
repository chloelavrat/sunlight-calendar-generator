# sunlight-calendar-generator

Generate iCal calendar files with daily sunrise, sunset, and daylight duration information for any location worldwide.

## Features

* Generate iCal calendar files with sunrise, sunset, and daylight duration
* Choose from hundreds of pre-configured cities worldwide
* Flexible date ranges and timezone support
* Handles polar night/midnight sun conditions

## How it Works

The app uses the `astral` library to calculate sunrise and sunset times based on geographic coordinates, then generates iCal (`.ics`) files that can be imported into any calendar application.

## Run app locally

1. **Run the app directly in a virtual environment**  
   ```bash
   git clone https://github.com/chloelavrat/sunlight-calendar-generator.git
   cd sunlight-calendar-generator
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```

2. **Run the app using docker**  
   ```bash
   docker build -t sunlight-calendar-generator .
   docker run -p 8501:8501 sunlight-calendar-generator
   ```
   Go to your web browser and access localhost:8501

## Contributing

Contributions are welcome! Submit a pull request or create an issue on the project's GitHub page.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
