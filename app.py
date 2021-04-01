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

city = input("Please enter a city: ")
address= 'city'
geolocator = Nominatim(user_agent="Your_Name")
location = geolocator.geocode(address)

lat = location.latitude
lon = location.longitude

import requests
api_key = 'aad6e7a0184b7699b8dbd1f773f442d8'
url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}&units=metric'
data = requests.get(url).json()

#temperature information
current.temperature = data['current']['temp']
hourly.temperature = data['hourly']['temp']
daily.temperature.day = data['daily']['temp']['day']
daily.temperature.min = data['daily']['temp']['min']
daily.temperature.max = data['daily']['temp']['max']
daily.temperature.night = data['daily']['temp']['night']

#weather information
current.weather.description = data['current']['weather']['description']
current.weather.icon = data['current']['weather']['icon']
hourly.weather.description = data['hourly']['weather']['description']
hourly.weather.description = data['hourly']['weather']['icon']
daily.weather.description = data['daily']['weather']['description']
daily.weather.icon = data['daily']['weather']['icon']

#rain information
minutely.precipitation = data['minutely']['precipitation']
current.rain = data['current']['rain']
hourly.rain = data['hourly']['rain']
daily.rain = data['daily']['rain']
















'''2. Block (Deniz)
Alle relevanten Darstellungen zu Temp (Python: seaborn, plotly, …)'''
def run_app():
    '''execute the whole program'''
    def plot_temp(lat, lon, temp):
        







'''3. Block (Elena)
Alle relevanten Darstellungen zu Nds (Python: seaborn, plotly, …)'''








'''4. Block (Julian)
Verbindung der relevanten Darstellungen zu Temp und Nds auf WebApp (Streamlit, HTML, CSS, Bootstrap, JS)'''
