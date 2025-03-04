from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

API_KEY = "53a5396fe9db3e56541140943600db10"  
BASE_URL = "https://api.openweathermap.org/data/2.5/"

def fetch_weather(city, forecast=False):
    endpoint = "forecast" if forecast else "weather"
    url = f"{BASE_URL}{endpoint}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if forecast:
            return [entry["main"]["temp"] for entry in data["list"][:5]] 
        return data["main"]["temp"]
    return None

@api_view(['GET'])
def current_weather(request, city):
    temp = fetch_weather(city)
    if temp is not None:
        return Response({"city": city, "temperature": temp})
    return Response({"error": "City not found"}, status=404)

@api_view(['GET'])
def forecast_weather(request, city):
    temps = fetch_weather(city, forecast=True)
    if temps is not None:
        return Response({"city": city, "forecast_temperatures": temps})
    return Response({"error": "City not found"}, status=404)