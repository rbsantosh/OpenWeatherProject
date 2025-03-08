from collections import defaultdict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import weatherData
from .serializers import WeatherDataSerializer
from django.utils.timezone import now
import requests

API_KEY = "53a5396fe9db3e56541140943600db10"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

def fetch_weather(city, forecast=False):
    cache_key = f"weather_{city}_{'forecast' if forecast else 'current'}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    weather = weatherData.objects.filter(city=city).first()
    is_outdated = weather and (now() - weather.latest_update).seconds >= 600

    endpoint = "forecast" if forecast else "weather"
    url = f"{BASE_URL}{endpoint}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if forecast:
            daily_temps = {}

            for entry in data["list"]:
                date = entry["dt_txt"].split()[0]  
                if date not in daily_temps:
                    daily_temps[date] = entry["main"]["temp"]  
                
                if len(daily_temps) == 5:  
                    break
            
            temp = list(daily_temps.values())

            if weather:
                weather.forecast_Data = temp
            else:
                weather = weatherData.objects.create(city=city, temprature=0.0, forecast_Data=temp)

        else:
            temp = data["main"]["temp"]
            if weather:
                weather.temprature = temp
            else:
                weather = weatherData.objects.create(city=city, temprature=temp, forecast_Data=None)

        weather.latest_update = now()
        weather.save()
        cache.set(cache_key, temp, timeout=600)
        return temp

    return None  

@cache_page(600)
@api_view(['GET'])
def current_weather(request, city):
    temp = fetch_weather(city, forecast=False)
    weather = weatherData.objects.filter(city=city).first()

    if weather:
        serializer = WeatherDataSerializer(weather, fields=['city', 'temprature']) 
        return Response(serializer.data)

    return Response({"error": "City not found"}, status=404)

@api_view(['GET'])
def forecast_weather(request, city):
    temp = fetch_weather(city, forecast=True)
    weather = weatherData.objects.filter(city=city).first()

    if weather and weather.forecast_Data:
        serializer = WeatherDataSerializer(weather, fields=['city', 'forecast_Data'])  
        return Response(serializer.data)

    return Response({"error": "City not found"}, status=404)
