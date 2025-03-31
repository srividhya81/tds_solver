import requests
import logging

import json
from urllib.parse import urlencode

from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

def get_weather_forecast(city_name):
    """
    Fetch the weather forecast for a given city using the BBC Weather API.

    Args:
        city_name (str): The name of the city to fetch the weather forecast for.

    Returns:
        dict: A JSON object mapping each localDate to its corresponding enhancedWeatherDescription.
    """
    try:
        # Step 1: Get the locationId for the city
        locator_url = "https://locator-service.api.bbci.co.uk/locations"
        locator_params = {
            "api_key": "AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv",  # Replace with your actual API key
            "locale": "en",
            "filter": "international",
            "q": city_name
        }

        locator_response = requests.get(locator_url, params=locator_params)
        locator_response.raise_for_status()
        locator_data = locator_response.json()

        if not locator_data or "location" not in locator_data or not locator_data["location"]:
            raise ValueError(f"No locationId found for city: {city_name}")

        location_id = locator_data["location"][0]["id"]

        # Step 2: Get the weather forecast using the locationId
        weather_url = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/{location_id}"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        if "forecasts" not in weather_data:
            raise ValueError(f"No forecast data found for locationId: {location_id}")

        # Step 3: Extract and transform the weather data
        forecast_json = {}
        for forecast in weather_data["forecasts"]:
            local_date = forecast.get("localDate")
            enhanced_description = forecast.get("enhancedWeatherDescription")
            if local_date and enhanced_description:
                forecast_json[local_date] = enhanced_description

        return forecast_json

    except Exception as e:
        logging.error(f"Error fetching weather forecast: {e}")
        return {"error": str(e)}
    


