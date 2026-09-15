import requests


def calculator(expression):
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return result

    except Exception:
        return "Sorry, I could not calculate that."


def get_weather(city):
    try:
        # Step 1: Find the city's latitude and longitude
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=30
        )

        geo_data = geo_response.json()

        if "results" not in geo_data:
            return f"Sorry, I could not find the city: {city}"

        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]

        # Step 2: Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=30
        )

        weather_data = weather_response.json()

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]

        return {
            "city": city,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed
        }

    except Exception as e:
        return f"Weather service error: {e}"