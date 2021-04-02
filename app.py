'''import libraries'''
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px








'''1. Block (Janina)
API anknüpfen (Python: json,...)
Input des Nutzers einlesen
Data handling (Python: pandas, numpy, ...) -> Alle Daten strukturiert eingelesen'''

import geopy
from geopy.geocoders import Nominatim

address = input("Please enter a city: ")
geolocator = Nominatim(user_agent="Your_Name")
location = geolocator.geocode(address)

lat = location.latitude
lon = location.longitude

import requests
api_key = 'aad6e7a0184b7699b8dbd1f773f442d8'
part = ['alerts']
url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}&units=metric'
data = requests.get(url).json()

#temperature information
current_temperature = data['current']['temp']
hourly_temperature = data['hourly']['temp']
daily_temperature_day = data['daily']['temp']['day']
daily_temperature_min = data['daily']['temp']['min']
daily_temperature_max = data['daily']['temp']['max']
daily_temperature_night = data['daily']['temp']['night']

#weather information
current_weather_description = data['current']['weather']['description']
current_weather_icon = data['current']['weather']['icon']
hourly_weather_description = data['hourly']['weather']['description']
hourly_weather_description = data['hourly']['weather']['icon']
daily_weather_description = data['daily']['weather']['description']
daily_weather_icon = data['daily']['weather']['icon']

#rain information
minutely_precipitation = data['minutely']['precipitation']
current_rain = data['current']['rain']
hourly_rain = data['hourly']['rain']
daily_rain = data['daily']['rain']
















'''2. Block (Deniz)
Alle relevanten Darstellungen zu Temp (Python: seaborn, plotly, …)'''
def run_app():
    '''execute the whole program'''
    def plot_temp(lat, lon, temp):
        







'''3. Block (Elena)
Alle relevanten Darstellungen zu Nds (Python: seaborn, plotly, …)'''








'''4. Block (Julian)
Verbindung der relevanten Darstellungen zu Temp und Nds auf WebApp (Streamlit, HTML, CSS, Bootstrap, JS)'''
