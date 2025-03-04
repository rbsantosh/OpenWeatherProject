from django.urls import path
from weather import views

urlpatterns = [
    path('current/<str:city>/',views.current_weather , name='current_weather'),
    path('forecast/<str:city>/', views.forecast_weather, name='forecast_weather'),
]