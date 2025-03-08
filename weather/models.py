from django.db import models
from django.utils.timezone import now

# Create your models here.
class weatherData(models.Model):
    city = models.CharField(max_length=100, unique=True)
    temprature = models.FloatField()
    forecast_Data= models.JSONField(null=True, blank=True)
    latest_update = models.DateTimeField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city