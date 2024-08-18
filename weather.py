import requests

def get_weather(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_data = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            # Add more fields as needed
        }
        return weather_data
    else:
        print("Failed to fetch weather data")
        return None

# API key for OpenWeatherMap (replace with your own key)
api_key = 'f87b83c744095c3b26aa0b1d6ddd64fc'
city = 'Pune, India'  # Example: 'New York, US'

weather_data = get_weather(api_key, city)
if weather_data:
    print("Real-time Weather Data:")
    print(f"Temperature: {weather_data['temperature']}°C")
    print(f"Humidity: {weather_data['humidity']}%")