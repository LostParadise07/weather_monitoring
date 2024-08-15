from django.db import models

class WeatherUpdate(models.Model):
    city = models.CharField(max_length=100)
    main_condition = models.CharField(max_length=100)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['-timestamp']

class DailyWeatherSummary(models.Model):
    date = models.DateField()
    city = models.CharField(max_length=100)
    average_temperature = models.FloatField()
    max_temperature = models.FloatField()
    min_temperature = models.FloatField()
    dominant_condition = models.CharField(max_length=100)
