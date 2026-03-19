import rumps
import subprocess
import threading
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import (
    get_weather, get_status_emoji, get_current_slack_status,
    is_weather_status, set_slack_status,
    SLACK_OAUTH_TOKEN, OPENWEATHER_API_KEY,
    LOCATION_CITY, LOCATION_COUNTRY, UNITS,
)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRON_COMMAND = f"source ~/.zprofile && {PROJECT_DIR}/.venv/bin/python {PROJECT_DIR}/src/main.py >> /tmp/slack-weather-status.log 2>&1"
CRON_SCHEDULE = "0 */4 * * *"
CRON_LINE = f"{CRON_SCHEDULE} {CRON_COMMAND}"


def get_crontab_lines():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if result.returncode != 0:
        return []
    return result.stdout.strip().split("\n") if result.stdout.strip() else []


def write_crontab(lines):
    text = "\n".join(lines) + "\n" if lines else ""
    subprocess.run(["crontab", "-"], input=text, text=True)


def get_cron_state():
    for line in get_crontab_lines():
        if CRON_COMMAND in line:
            if line.strip().startswith("#"):
                return "paused"
            return "running"
    return "stopped"


def set_cron_state(target):
    lines = [l for l in get_crontab_lines() if CRON_COMMAND not in l]
    if target == "running":
        lines.append(CRON_LINE)
    elif target == "paused":
        lines.append(f"# {CRON_LINE}")
    write_crontab(lines)


def run_weather_update():
    current_emoji, _ = get_current_slack_status(SLACK_OAUTH_TOKEN)
    if not is_weather_status(current_emoji):
        rumps.notification("Weather Status", "Skipped", "Custom status is set")
        return
    weather = get_weather(OPENWEATHER_API_KEY, LOCATION_CITY, LOCATION_COUNTRY, UNITS)
    if weather:
        temp = round(weather['main']['temp'])
        description = weather['weather'][0]['description']
        status_text = f"{temp}°C & {description.capitalize()} in {LOCATION_CITY}"
        status_emoji = get_status_emoji(weather)
        set_slack_status(SLACK_OAUTH_TOKEN, status_text, status_emoji)
        rumps.notification("Weather Status", "Updated", f"{status_emoji} {status_text}")


def clear_slack_status():
    set_slack_status(SLACK_OAUTH_TOKEN, "", "")


ICONS = {"running": "☀️", "paused": "⏸", "stopped": "⏹"}


class WeatherStatusApp(rumps.App):
    def __init__(self):
        state = get_cron_state()
        super().__init__(ICONS.get(state, "WX"), quit_button="Quit")
        self.status_display = rumps.MenuItem(f"State: {state.capitalize()}")
        self.menu = [
            rumps.MenuItem("Run"),
            rumps.MenuItem("Pause"),
            rumps.MenuItem("Stop"),
            None,
            self.status_display,
        ]

    def refresh_ui(self):
        state = get_cron_state()
        self.title = ICONS.get(state, "WX")
        self.status_display.title = f"State: {state.capitalize()}"

    @rumps.clicked("Run")
    def on_run(self, _):
        set_cron_state("running")
        self.refresh_ui()
        threading.Thread(target=run_weather_update, daemon=True).start()

    @rumps.clicked("Pause")
    def on_pause(self, _):
        set_cron_state("paused")
        self.refresh_ui()

    @rumps.clicked("Stop")
    def on_stop(self, _):
        set_cron_state("stopped")
        threading.Thread(target=clear_slack_status, daemon=True).start()
        self.refresh_ui()


if __name__ == "__main__":
    WeatherStatusApp().run()
