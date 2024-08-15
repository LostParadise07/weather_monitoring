from django.shortcuts import render
from weather.models import DailyWeatherSummary

from weather.models import WeatherUpdate, DailyWeatherSummary
import pandas as pd
def weather_summary(request):
    summaries = DailyWeatherSummary.objects.all()
    return render(request, 'weather/summary.html', {'summaries': summaries})


def generate_daily_summaries():
    updates = WeatherUpdate.objects.all()
    df = pd.DataFrame(list(updates.values()))
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    daily_summary = df.groupby(['date', 'city']).agg(
        average_temperature=('temperature', 'mean'),
        max_temperature=('temperature', 'max'),
        min_temperature=('temperature', 'min'),
        dominant_condition=('main_condition', lambda x: x.value_counts().idxmax())
    ).reset_index()

    for _, row in daily_summary.iterrows():
        DailyWeatherSummary.objects.update_or_create(
            date=row['date'],
            city=row['city'],
            defaults={
                'average_temperature': row['average_temperature'],
                'max_temperature': row['max_temperature'],
                'min_temperature': row['min_temperature'],
                'dominant_condition': row['dominant_condition']
            }
        )
