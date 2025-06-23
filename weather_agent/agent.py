import datetime
import os
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import requests
from typing import Optional
from google.adk.tools import google_search

def get_weather_for_plants(city: str, country_code: Optional[str] = None) -> dict:
    """
    Get weather data relevant for plant growing conditions
    
    Args:
        city: City name
        api_key: OpenWeatherMap API key
        country_code: Optional ISO country code (e.g., 'US', 'GB')
    
    Returns:
        Dict: Weather data focused on plant growing conditions
    """
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        location = f"{city},{country_code}" if country_code else city
        
        params = {
            'q': location,
            'appid': os.getenv('OPENWEATHERMAP_API_KEY'),
            'units': 'metric'
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        weather_data = {
            'location': {
                'city': data['name'],
                'country': data['sys']['country'],
                'coordinates': {
                    'lat': data['coord']['lat'],
                    'lon': data['coord']['lon']
                }
            },
            'temperature': {
                'current_c': data['main']['temp'],
                'feels_like_c': data['main']['feels_like'],
                'min_c': data['main']['temp_min'],
                'max_c': data['main']['temp_max']
            },
            'humidity_percent': data['main']['humidity'],
            'pressure_hpa': data['main']['pressure'],
            'wind': {
                'speed_ms': data['wind']['speed'],
                'direction_deg': data['wind'].get('deg', 0),
                'gust_ms': data['wind'].get('gust', 0)
            },
            'clouds': {
                'coverage_percent': data['clouds']['all']
            },
            'visibility_m': data.get('visibility', 0),
            'weather': {
                'main': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            },
            'precipitation': {
                'rain_1h_mm': data.get('rain', {}).get('1h', 0),
                'rain_3h_mm': data.get('rain', {}).get('3h', 0),
                'snow_1h_mm': data.get('snow', {}).get('1h', 0),
                'snow_3h_mm': data.get('snow', {}).get('3h', 0)
            }
        }

        city_name = weather_data['location']['city']
        country = weather_data['location']['country']
        temp = weather_data['temperature']['current_c']
        desc = weather_data['weather']['description'].capitalize()
        humidity = weather_data['humidity_percent']
        wind = weather_data['wind']['speed_ms']
        clouds = weather_data['clouds']['coverage_percent']

        report = (
            f"The weather in {city_name}, {country} is {desc} "
            f"with a temperature of {temp} degrees Celsius, "
            f"humidity of {humidity}%, wind speed of {wind} m/s, "
            f"and cloud cover of {clouds}%."
        )
        if(report):
            return {
                "status": "success",
                "report": report
            }
    
        else:
            return {
                "status": "error",
                "error_message": f"Weather information for '{city}' is not available."
            }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"API request failed: {str(e)}"
        }
    except KeyError as e:
        return {
            "status": "error",
            "error_message": f"Missing data in API response: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error: {str(e)}"
        }

root_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    description=(
    "A friendly, knowledgeable agent designed to provide up-to-date and detailed weather information "
    "for any given city or country, with a special focus on helping users grow flowers and plants. "
    "This agent reports not just the basic weather summary, but also key environmental conditions important for plant health—"
    "including temperature, humidity, wind speed and direction, precipitation, sunlight hours, cloud cover, and more. "
    "Whether you're a gardener, farmer, or simply a plant lover, this agent ensures you get the right data to support healthy and successful plant growth, "
    "wherever you are in the world."
   ),
    instruction=(
    "You are a polite, helpful, and approachable agent whose main role is to answer user questions "
    "about the current weather in any city or country, with extra detail for those interested in growing flowers or plants. "
    "When a user requests weather information, fetch the latest and most detailed weather data for the given location, "
    "and summarize it in a clear, concise, and friendly way. Focus on reporting conditions relevant to plant growth, such as temperature, humidity, "
    "wind, precipitation (rain/snow), cloud cover, sunlight (sunrise/sunset), and atmospheric pressure. "
    "Always be respectful and welcoming in your responses, making sure users feel comfortable and supported. "
    "If the location is unclear or unavailable, kindly ask for clarification. "
    "Your mission is to empower users to care for their flowers and plants with accurate, useful, and accessible weather updates."
    ),
    tools=[get_weather_for_plants],
)

