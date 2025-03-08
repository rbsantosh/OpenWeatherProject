from rest_framework import serializers
from .models import weatherData



class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = weatherData
        fields = ['city', 'temprature', 'forecast_Data']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(WeatherDataSerializer, self).__init__(*args, **kwargs)

        if fields:
            for field in set(self.fields) - set(fields):
                self.fields.pop(field)