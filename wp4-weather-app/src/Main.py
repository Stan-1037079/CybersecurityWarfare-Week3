from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import sqlite3

app = Flask(__name__)
CORS(app)
app.debug = True

@app.route('/api/weather')
def get_weather():
    location = request.args.get('location')
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid=11b4c7f160b27a5f817bbfa076f221b4"
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        return jsonify(data)
    else: 
        return jsonify({'cod': data['cod']})

@app.route('/api/forecast')
def get_forecast():
    location = request.args.get('location')
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid=11b4c7f160b27a5f817bbfa076f221b4"
    response = requests.get(url)
    geocoding_data = response.json()
    if geocoding_data:
        lat = geocoding_data[0]['lat']
        lon = geocoding_data[0]['lon']
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid=11b4c7f160b27a5f817bbfa076f221b4"
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        return jsonify(forecast_data)
    else:
        return jsonify({'message': 'Location not found'})

@app.route('/api/saveinput', methods=['POST'])
def save_inputs():
    conn = sqlite3.connect('Weatherdatabase.db')
    cursor = conn.cursor()
    location = request.json.get('location')
    rain_chance = request.json.get('rainChanceinput')
    max_temp = request.json.get('maxTemp')
    min_temp = request.json.get('minTemp')
    snow_chance = request.json.get('snowChanceinput')
    max_wind_speed = request.json.get('maxWindSpeed')
    cursor.execute('''
        INSERT INTO inputs (location, rain_chance, max_temp, min_temp, snow_chance, max_wind_speed)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (location, rain_chance, max_temp, min_temp, snow_chance, max_wind_speed))
    conn.commit()
    return jsonify({'message': 'Inputs saved in the Database'})
    
if __name__ == '__main__':
    app.run(debug=True)