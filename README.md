# slack-weather-status

Sets your Slack profile status to the current weather in your area (emoji + temperature + conditions).

## Setup

1. Create a [Slack app](https://api.slack.com/apps) with the `users.profile:write` user token scope
2. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
3. Add both to your shell profile (e.g. `~/.zprofile`):

```bash
export SLACK_API_TOKEN_WEATHER="xoxp-your-token"
export OPENWEATHER_API_KEY="your-key"
```

4. Set up the venv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
source .venv/bin/activate
python main.py
```

Edit `LOCATION_CITY` and `LOCATION_COUNTRY` in `main.py` to change the location.
