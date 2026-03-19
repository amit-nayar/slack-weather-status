<p align="center">
  <img src="assets/repo-icon.png" width="128" alt="slack-weather-status">
</p>

# slack-weather-status

Sets your Slack profile status to the current weather in your area (emoji + temperature + conditions). Runs on a schedule via cron and includes a macOS menu bar app to control it.

![Example](assets/screenshot.png)

## How it works

- Fetches current weather from OpenWeatherMap
- Maps conditions to Slack emojis (sun, rain, snow, fog, clouds, etc.)
- Sets your Slack status, e.g. `:sunny: 15°C & Clear sky in Stuttgart`
- Status auto-expires after 4 hours
- If you've manually set a non-weather status, it won't overwrite it

## Setup

1. Create a [Slack app](https://api.slack.com/apps) with the `users.profile:write` and `users.profile:read` user token scopes
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

Run once manually:

```bash
.venv/bin/python src/main.py
```

### Menu bar app

Launch the macOS menu bar app for easy control:

```bash
.venv/bin/python src/menubar.py
```

![Menu bar demo](assets/demo.gif)

The menu bar icon shows the current state:

| Icon | State | Description |
|------|-------|-------------|
| ☀️ | Running | Cron active, status updates every 4 hours |
| ⏸ | Paused | Cron disabled, current status stays |
| ⏹ | Stopped | Cron disabled, status cleared |

The menu bar app starts automatically at login via a LaunchAgent.

## Configuration

Edit `LOCATION_CITY` and `LOCATION_COUNTRY` in `src/main.py` to change the location.
