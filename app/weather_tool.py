# Copyright 2026 Google LLC
# Real live weather forecast tool powered by Open-Meteo API (Free, no API key required)

import json
import urllib.parse
import urllib.request
from typing import Any, Dict

WMO_WEATHER_CODES = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️",
    2: "Partly cloudy ⛅",
    3: "Overcast ☁️",
    45: "Foggy 🌫️",
    48: "Depositing rime fog 🌫️",
    51: "Light drizzle 🌧️",
    53: "Moderate drizzle 🌧️",
    55: "Dense drizzle 🌧️",
    61: "Slight rain 🌧️",
    63: "Moderate rain 🌧️",
    65: "Heavy rain 🌧️",
    71: "Slight snow 🌨️",
    73: "Moderate snow 🌨️",
    75: "Heavy snow 🌨️",
    80: "Slight rain showers 🌦️",
    81: "Moderate rain showers 🌦️",
    82: "Violent rain showers ⛈️",
    95: "Thunderstorm 🌩️",
    96: "Thunderstorm with slight hail ⛈️",
    99: "Thunderstorm with heavy hail ⛈️",
}


def get_live_weather(destination: str) -> Dict[str, Any]:
    """Fetch real-time weather and 3-day forecast for any travel destination worldwide.

    Args:
        destination: Name of destination city or location (e.g. 'Tokyo', 'Paris', 'New York', 'Kyoto').

    Returns:
        Dict with live current temperature (°C / °F), weather description, wind speed, humidity, and 3-day forecast.
    """
    try:
        # Step 1: Geocode city name to lat/lon using Open-Meteo Geocoding API
        encoded_dest = urllib.parse.quote(destination.strip())
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_dest}&count=1&language=en&format=json"

        req = urllib.request.Request(geo_url, headers={"User-Agent": "easy-travel-agent/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            geo_data = json.loads(response.read().decode())

        if not geo_data.get("results"):
            return {"error": f"Could not find geographic coordinates for destination '{destination}'."}

        location_info = geo_data["results"][0]
        lat = location_info["latitude"]
        lon = location_info["longitude"]
        city_name = location_info.get("name", destination.title())
        country = location_info.get("country", "")

        # Step 2: Fetch current & forecast weather from Open-Meteo
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
            f"&daily=weather_code,temperature_2m_max,temperature_2m_min"
            f"&forecast_days=3&timezone=auto"
        )

        w_req = urllib.request.Request(weather_url, headers={"User-Agent": "easy-travel-agent/1.0"})
        with urllib.request.urlopen(w_req, timeout=5) as w_resp:
            weather_data = json.loads(w_resp.read().decode())

        current = weather_data.get("current", {})
        daily = weather_data.get("daily", {})

        temp_c = current.get("temperature_2m", 20.0)
        temp_f = round((temp_c * 9 / 5) + 32, 1)
        w_code = current.get("weather_code", 0)
        condition = WMO_WEATHER_CODES.get(w_code, "Pleasant Weather")
        humidity = current.get("relative_humidity_2m", 50)
        wind_kmh = current.get("wind_speed_10m", 10)

        # Build 3-day forecast
        forecast_dates = daily.get("time", [])
        forecast_max_c = daily.get("temperature_2m_max", [])
        forecast_min_c = daily.get("temperature_2m_min", [])
        forecast_codes = daily.get("weather_code", [])

        three_day_forecast = []
        for i in range(min(3, len(forecast_dates))):
            min_f = round((forecast_min_c[i] * 9 / 5) + 32, 1) if i < len(forecast_min_c) else N/A
            max_f = round((forecast_max_c[i] * 9 / 5) + 32, 1) if i < len(forecast_max_c) else N/A
            code = forecast_codes[i] if i < len(forecast_codes) else 0
            three_day_forecast.append({
                "date": forecast_dates[i],
                "condition": WMO_WEATHER_CODES.get(code, "Clear"),
                "low_temp_f": min_f,
                "high_temp_f": max_f,
            })

        # Packing recommendations based on temperature & rain
        packing_tips = []
        if temp_f < 50:
            packing_tips.append("Warm coat, thermal layers, beanie, and gloves.")
        elif temp_f < 68:
            packing_tips.append("Light jacket, sweater, and long pants.")
        else:
            packing_tips.append("Light breathable clothing, sunglasses, and sunscreen.")

        if w_code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]:
            packing_tips.append("Compact umbrella or waterproof raincoat.")

        return {
            "destination": f"{city_name}, {country}".strip(", "),
            "current_weather": {
                "temperature_c": temp_c,
                "temperature_f": temp_f,
                "condition": condition,
                "humidity_percent": humidity,
                "wind_speed_kmh": wind_kmh,
            },
            "packing_recommendations": " ".join(packing_tips),
            "three_day_forecast": three_day_forecast,
            "data_source": "Open-Meteo Live Global Weather API",
        }
    except Exception as e:
        return {"error": f"Failed to fetch live weather data for '{destination}': {str(e)}"}
