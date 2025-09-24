import requests
import json
import os
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# IMPORTANT: Use environment variables in a real application for security.
SLACK_OAUTH_TOKEN = "xoxp-YOUR-SLACK-OAUTH-TOKEN"  # Paste your token here
OPENWEATHER_API_KEY = "YOUR-OPENWEATHER-API-KEY" # Paste your API key here
LOCATION_CITY = "Stuttgart"
LOCATION_COUNTRY = "DE"
UNITS = "metric"  # Use "imperial" for Fahrenheit

def get_weather(api_key, city, country, units):
    """Fetches weather data from OpenWeatherMap."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': f'{city},{country}',
        'appid': api_key,
        'units': units
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None

def get_status_emoji(weather_data):
    """Selects a Slack emoji based on the weather condition."""
    if not weather_data:
        return ":question:"

    weather_id = weather_data['weather'][0]['id']
    
    # Weather condition codes from OpenWeatherMap
    if 200 <= weather_id <= 232:
        return ":thunder_cloud_and_rain:"
    elif 300 <= weather_id <= 321:
        return ":drizzle:"
    elif 500 <= weather_id <= 531:
        return ":rain_cloud:"
    elif 600 <= weather_id <= 622:
        return ":snowflake:"
    elif 701 <= weather_id <= 781:
        return ":fog:"
    elif weather_id == 800:
        return ":sunny:"
    elif 801 <= weather_id <= 804:
        return ":cloud:"
    else:
        return ":sun_behind_cloud:"

def set_slack_status(token, text, emoji):
    """Sets the user's status in Slack."""
    url = "https://slack.com/api/users.profile.set"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    # Status expires at the end of the day
    end_of_day = datetime.now().replace(hour=23, minute=59, second=59)
    expiration_timestamp = int(end_of_day.timestamp())

    payload = {
        "profile": {
            "status_text": text,
            "status_emoji": emoji,
            "status_expiration": expiration_timestamp
        }
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        if result.get("ok"):
            print("Successfully updated Slack status!")
        else:
            print(f"Failed to update Slack status: {result.get('error')}")
    except requests.exceptions.RequestException as e:
        print(f"Error setting Slack status: {e}")


if __name__ == "__main__":
    weather = get_weather(OPENWEATHER_API_KEY, LOCATION_CITY, LOCATION_COUNTRY, UNITS)
    
    if weather:
        temp = round(weather['main']['temp'])
        description = weather['weather'][0]['description']
        
        status_text = f"{temp}°C & {description.capitalize()} in {LOCATION_CITY}"
        status_emoji = get_status_emoji(weather)
        
        print(f"Setting status to: {status_emoji} {status_text}")
        set_slack_status(SLACK_OAUTH_TOKEN, status_text, status_emoji)
