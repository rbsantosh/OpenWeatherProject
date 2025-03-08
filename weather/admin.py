from django.contrib import admin
from .models import weatherData

class weatherAdmin(admin.ModelAdmin):
    list_display = [
        "city",
        "temprature",
        "forecast_Data",
        "created_at",
    ]
   
    search_fields = ["city"]
    
admin.site.register(weatherData, weatherAdmin)

