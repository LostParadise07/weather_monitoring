import requests
from django.core.management.base import BaseCommand
from weather.models import WeatherUpdate
from django.utils import timezone
from decouple import config

class Command(BaseCommand):
    help = 'Fetch weather data from OpenWeatherMap API'

    def handle(self, *args, **kwargs):
        api_key = config('OPENWEATHER_API_KEY')
        cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
        for city in cities:
            try:
                response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}')
                data = response.json()

                # Print the response to check its structure
                print(f"Response for {city}: {data}")

                # Handle possible errors
                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f"Failed to fetch data for {city}: {data.get('message', 'Unknown error')}"))
                    continue

                # Check if 'weather' key exists
                if 'weather' not in data:
                    self.stdout.write(self.style.ERROR(f"Missing 'weather' key in response for {city}"))
                    continue

                # Save weather update
                weather_update = WeatherUpdate(
                    city=city,
                    main_condition=data['weather'][0]['main'],
                    temperature=data['main']['temp'] - 273.15,  # Convert Kelvin to Celsius
                    feels_like=data['main']['feels_like'] - 273.15,  # Convert Kelvin to Celsius
                    timestamp=timezone.datetime.fromtimestamp(data['dt'])
                )
                weather_update.save()

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred for {city}: {str(e)}"))
