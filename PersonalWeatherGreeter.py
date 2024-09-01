import pyttsx3
import datetime
import requests
import pyautogui
import time

def minimize_terminal():
    time.sleep(1)
    pyautogui.hotkey('win', 'down')

def get_location():
    try:
        ipinfo_response = requests.get("https://ipinfo.io")
        location_data = ipinfo_response.json()
        loc = location_data["loc"].split(',')
        latitude = loc[0]
        longitude = loc[1]
        city = location_data.get("city", "Unknown City")
        region = location_data.get("region", "Unknown Region")
        country = location_data.get("country", "Unknown Country")
        return latitude, longitude, city, region, country
    except:
        return "39.3735", "-86.0530", "Unknown City", "Unknown Region", "Unknown Country"

def get_weather():
    latitude, longitude, city, region, country = get_location()
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&daily=weathercode,precipitation_probability_mean&timezone=auto"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        
        current_weather = data.get("current_weather", {})
        temperature_celsius = current_weather.get("temperature", "N/A")
        wind_speed_ms = current_weather.get("windspeed", "N/A")
        weather_code = current_weather.get("weathercode", "N/A")
        
        temperature_fahrenheit = (temperature_celsius * 9/5) + 32
        wind_speed_mph = wind_speed_ms * 2.237
        
        daily = data.get("daily", {})
        weather_code_daily = daily.get("weathercode", [])[0]
        precipitation_probability = daily.get("precipitation_probability_mean", [])[0]
        
        weather_conditions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Drizzle: Light",
            53: "Drizzle: Moderate",
            55: "Drizzle: Dense intensity",
            56: "Freezing Drizzle: Light",
            57: "Freezing Drizzle: Dense intensity",
            61: "Rain: Slight",
            63: "Rain: Moderate",
            65: "Rain: Heavy intensity",
            66: "Freezing Rain: Light",
            67: "Freezing Rain: Heavy intensity",
            71: "Snow fall: Slight",
            73: "Snow fall: Moderate",
            75: "Snow fall: Heavy intensity",
            77: "Snow grains",
            80: "Rain showers: Slight",
            81: "Rain showers: Moderate",
            82: "Rain showers: Violent",
            85: "Snow showers slight",
            86: "Snow showers heavy",
            95: "Thunderstorm: Slight or moderate",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        sky_condition = weather_conditions.get(weather_code, "Unknown")
        sky_condition_daily = weather_conditions.get(weather_code_daily, "Unknown")
        
        weather_info = (f"Current temperature is {temperature_fahrenheit:.1f}°F with a wind speed of {wind_speed_mph:.1f} mph, "
                        f"Sky condition is {sky_condition}, "
                        f"Chance of rain is: {precipitation_probability:.1f}%. "
                        f"Today's forecast is: {sky_condition_daily}.")
        
        location_info = f"{city}, {region}, {country}"
        return weather_info, location_info
    else:
        return "Unable to fetch weather information.", "Unknown Location"

def get_time_of_day():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 18:
        return "afternoon"
    elif 18 <= current_hour < 22:
        return "evening"
    else:
        return "night"

def greet_user():
    engine = pyttsx3.init()
    engine.setProperty('voice', 'english_rp+f4')

    current_time = datetime.datetime.now().strftime("%I:%M %p")
    time_of_day = get_time_of_day()
    weather_info, location_info = get_weather()

    if time_of_day != "night":
        greeting_message = f"Good {time_of_day}, Welcome back sir. It is currently {current_time}. Here is your weather for {location_info} today: {weather_info}"
    else:
        greeting_message = f"Hello, Welcome back sir. It is currently {current_time}. Here is your weather for {location_info} tonight: {weather_info}" 

    if time_of_day == "morning":
        ending_message = "Have a wonderful morning."
    elif time_of_day == "afternoon":
        ending_message = "Have a wonderful afternoon."
    elif time_of_day == "evening":
        ending_message = "Have a wonderful evening."
    else:
        ending_message = "Have a pleasant night."

    full_message = f"{greeting_message} {ending_message}"

    engine.say(full_message)
    engine.runAndWait()

if __name__ == "__main__":
    minimize_terminal()
    greet_user()
