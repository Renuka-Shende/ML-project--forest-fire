from flask import Flask, request, render_template
import pickle
import numpy as np
import requests

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/fire')
def A():
    return render_template("forest_fire.html")


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final = [np.array(int_features)]
    print(int_features)
    print(final)
    prediction = model.predict_proba(final)
    output = '{0:.{1}f}'.format(prediction[0][1], 2)

    if output > str(0.5):
        return render_template('forest_fire.html', pred='Sign of Danger.\nProbability of fire occurring is {}'.format(output))
    else:
        return render_template('forest_fire.html', pred='The Forest is safe.\n Probability of fire occurring is {}'.format(output))

@app.route('/city', methods=['POST'])
def city():
    def get_weather_by_city(api_key, city):
            # url_weather = f'http://api.openweathermap.org/data/2.5/weather?lat={lati}&lon={longi}&appid={api_key}&units=metric'
        url_weather = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response_weather = requests.get(url_weather)
        data_weather = response_weather.json()
        if response_weather.status_code == 200:
            weather_data = {
                'temperature': data_weather['main']['temp'],
                'humidity': data_weather['main']['humidity'],
                'wind_speed': data_weather['wind']['speed'],
                'weather_description': data_weather['weather'][0]['description'],
                'cloudiness': data_weather['clouds']['all'],
                
                # Add more fields as needed
            }
            return weather_data
            
        else:
            print("Failed to fetch weather data")
        # Default response in case of error
        return {
            'temperature': 'N/A',
            'humidity': 'N/A',
            'wind_speed': 'N/A',
            'weather_description': 'N/A',
            'cloudiness': 'N/A',
            'oxygen_level': 'N/A',
        }
    
    def get_weather_by_longi(api_key, longi, lati):
        url_weather = f'http://api.openweathermap.org/data/2.5/weather?lat={lati}&lon={longi}&appid={api_key}'
        response_weather = requests.get(url_weather)
        data_weather = response_weather.json()
        print("status:")
        print(response_weather.status_code)
        # if data_weather["cod"] != 404:
        if response_weather.status_code == 200:
            weather_data = {
                'temperature': data_weather['main']['temp'] -273.15,
                'humidity': data_weather['main']['humidity'],
                'wind_speed': data_weather['wind']['speed'],
                'weather_description': data_weather['weather'][0]['description'],
                'cloudiness': data_weather['clouds']['all'],
                
                # Add more fields as needed
            }
            # weather_data['temperature']=(weather_data['temperature']-32)/1.8
            return weather_data
            
        else:
            print("Failed to fetch weather data")
        # Default response in case of error
        return {
            'temperature': 'N/A',
            'humidity': 'N/A',
            'wind_speed': 'N/A',
            'weather_description': 'N/A',
            'cloudiness': 'N/A',
            'oxygen_level': 'N/A',
        }

    open_weather_api_key = 'f87b83c744095c3b26aa0b1d6ddd64fc'
    city = request.form['city_name']
    longi = request.form['longitude']
    lati = request.form['latitude']
    if city=="":
          # Example: 'New York, US'
        weather_data = get_weather_by_longi(open_weather_api_key, longi, lati)
        
    else:
        weather_data = get_weather_by_city(open_weather_api_key, city)
        
        
    # else:
    #     print("Neither city name nor latitude/longitude provided")


    
    return render_template('weather.html', temp=weather_data['temperature'], humidity=weather_data['humidity'],
                           wind_speed=weather_data['wind_speed'], weather_description=weather_data['weather_description'],
                           cloudiness=weather_data['cloudiness'])  #

@app.route('/weather')
def show_weather():
    return render_template('weather.html')



@app.route('/analysis')
def B():
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run(debug=True)
