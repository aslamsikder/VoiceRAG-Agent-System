import requests
import json
import random

class Tools:
    @staticmethod
    def get_current_weather(location: str):
        """
        Get the current weather for a given location using OpenMeteo (Free).
        """
        try:
            # 1. Geocoding to get lat/lon
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
            geo_res = requests.get(geo_url).json()
            
            if not geo_res.get("results"):
                return json.dumps({"error": "Location not found"})
            
            lat = geo_res["results"][0]["latitude"]
            lon = geo_res["results"][0]["longitude"]
            
            # 2. Weather Data
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_res = requests.get(weather_url).json()
            
            current = weather_res.get("current_weather", {})
            return json.dumps({
                "location": location,
                "temperature": current.get("temperature"),
                "windspeed": current.get("windspeed"),
                "unit": "Celsius"
            })
        except Exception as e:
            return json.dumps({"error": str(e)})

    @staticmethod
    def get_stock_price(ticker: str):
        """
        Get stock price (Mock/Free API simplified). 
        Simulating response for demonstration reliability.
        """
        price = round(random.uniform(100, 500), 2)
        return json.dumps({"ticker": ticker, "price": price, "currency": "USD"})

    # Tool Definitions for OpenAI
    tools_schema = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                    },
                    "required": ["location"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_stock_price",
                "description": "Get the current stock price of a company ticker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "The stock symbol (e.g., AAPL, TSLA)",
                        },
                    },
                    "required": ["ticker"],
                },
            },
        }
    ]