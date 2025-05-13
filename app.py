from flask import Flask, request, jsonify, render_template
import requests
import re
from datetime import datetime

app = Flask(__name__)
API_KEY = '36bf698c847fe95ecc5ba32d4f16ce1f'  # Your OpenWeather API key

# Helper function to get weather data from OpenWeather API
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

# Function to handle greetings
def handle_greetings(user_input):
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    for greeting in greetings:
        if greeting in user_input.lower():
            return "Hello! How can I assist you today? Ask about the current weather in your city! 🌤️"

    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    # Check for greetings
    greeting_response = handle_greetings(user_input)
    if greeting_response:
        return jsonify({'reply': greeting_response})

    # Extract the city name from the user input
    city_search = re.search(r'(in\s+)?(\w+)', user_input)
    if city_search:
        city = city_search.group(2).strip()
    else:
        return jsonify({'reply': "Please provide a city name."})

    # Get the current weather for the city
    data = get_weather_data(city)
    
    if data.get("main"):
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        icon = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon}.png"
        city_name = data["name"]
        
        weather_info = f"Current weather in {city_name}:\n"
        weather_info += f"🌡️ Temperature: {temperature}°C\n"
        weather_info += f"🌥️ Weather: {weather.capitalize()}\n"
        weather_info += f"<img src='{icon_url}' alt='Weather Icon'/>"
        
        return jsonify({'reply': weather_info})
    else:
        return jsonify({'reply': "City not found or invalid input. Please try again."})

if __name__ == '__main__':
    app.run(debug=True)
