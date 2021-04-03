'''import libraries'''
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import json








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
hourly_temperature = data['hourly'][0]['temp']
daily_temperature_day = data['daily'][0]['temp']['day']
daily_temperature_min = data['daily'][0]['temp']['min']
daily_temperature_max = data['daily'][0]['temp']['max']
daily_temperature_night = data['daily'][0]['temp']['night']

#weather information
current_weather_description = data['current']['weather'][0]['description']
hourly_weather_description = data['hourly'][0]['weather'][0]['description']
daily_weather_description = data['daily'][0]['weather'][0]['description']

#rain information
minutely_precipitation = data['minutely'][0]['precipitation']

#wind information
daily_wind_deg = data['daily'][0]['wind_deg']
daily_wind_speed = data['daily'][0]['wind_speed']
hourly_wind_deg = data['hourly'][0]['wind_deg']
hourly_wind_speed = data['hourly'][0]['wind_speed']
current_wind_deg = data['current']['wind_deg']
current_wind_speed = data['current']['wind_speed']
















'''2. Block (Deniz)
Alle relevanten Darstellungen zu Temp (Python: seaborn, plotly, …)'''
def run_app():
    '''execute the whole program'''
    #def plot_temp(lat, lon, temp):
        







'''3. Block (Elena)
Alle relevanten Darstellungen zu Nds (Python: seaborn, plotly, …)'''








'''4. Block (Julian)
Verbindung der relevanten Darstellungen zu Temp und Nds auf WebApp (Streamlit, HTML, CSS, Bootstrap, JS)'''
