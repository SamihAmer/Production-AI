"""
WeatherProxy: fetch current weather and publish to IoT Hub as device telemetry.
"""
from __future__ import annotations
import time, requests
from typing import Dict, Any
from dataclasses import dataclass
from ..iothub.iot_client import IoTHubClient

@dataclass
class WeatherProxy:
    city: str
    api_key: str
    iothub_device_conn_str: str
    device_id: str

    def fetch_weather(self) -> Dict[str, Any]:
        """Call OpenWeatherMap current weather endpoint and return normalized dict."""
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": self.city, "appid": self.api_key, "units": "metric"}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        j = r.json()
        return {
            "condition": j["weather"][0]["main"],
            "temp_c": j["main"]["temp"],
            "humidity": j["main"]["humidity"],
            "city": self.city,
        }

    def build_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"type": "weather", "device_id": self.device_id, "ts": int(time.time()), "payload": payload}

    def run_once(self) -> Dict[str, Any]:
        payload = self.fetch_weather()
        msg = self.build_message(payload)
        IoTHubClient(self.iothub_device_conn_str).send_message(msg)
        return msg
