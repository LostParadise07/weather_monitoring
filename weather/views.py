from django.shortcuts import render
from weather.models import DailyWeatherSummary

from weather.models import WeatherUpdate, DailyWeatherSummary
import pandas as pd
def weather_summary(request):
    summaries = DailyWeatherSummary.objects.all()
    updates = WeatherUpdate.objects.all()
    return render(request, 'weather/summary.html', {'summaries': summaries,'updates': updates})

