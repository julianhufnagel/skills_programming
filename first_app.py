import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import json
import geopy
from geopy.geocoders import Nominatim
import geocoder

#styling
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        footer:after {
        content:'Made with love by: Elena, Julian, Janina & Deniz'; 
        visibility: visible;
        display: block;
        position: relative;
        color: #12DEFF;
        }
        </style>
        """ 
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.image('./images/weatherapp.png')


# Functions

#'''define callable function for daily temperature with variables from the API'''
def daily_plot_temp(daily_temperature):
    df = pd.DataFrame(list(daily_temperature.items()),columns = ['Date','Temperature']) #gathered data from dict into Dataframe
    df[['day','min','max','night','morn']] = pd.DataFrame(df['Temperature'].to_list(), columns=['day','min', 'max', 'night', 'morn']) #split the data stored in the temperature list into individual columns
    del df['Temperature'] #delete column as information is now in seperate columns
    #plot min, max and day temperature in a diagramm (three lines)
    df = df.set_index("Date")[["day","min","max"]]
    return df

#'''define callable function requiring hourly temperature from the openweathermap API'''
def hourly_plot_temp(hourly_temperature):
    df = pd.DataFrame(list(hourly_temperature.items()),columns = ['Date/Time','Temperature']) #dictionary into dataframe
    #'''plotting the information with time on the X and Temperature on the Y axis'''
    df = df.set_index("Date/Time")
    return df

def daily_plot_wind(daily_wind_speed):
    df = pd.DataFrame(list(daily_wind_speed.items()),columns = ['Date/Time','Windspeed']) #dictionary into dataframe
    #'''plotting the information with time on the X and Windspeed on the Y axis'''
    df = df.set_index("Date/Time")
    return df

# Locate
geolocator = Nominatim(user_agent="Your_Name")
g = geocoder.ip('me')
your_location = geolocator.reverse(f"{g.lat},{g.lng}")
address = st.text_input("Please enter a city name", your_location)
st.button('Search')
location = geolocator.geocode(address)
captured_address = geolocator.reverse(f"{location.latitude},{location.longitude}")

try:
    lat = location.latitude
    lon = location.longitude
except:
    st.error("This city is not known to our system. Please try another city.")
    st.stop()



# Data import

import requests
api_key = 'aad6e7a0184b7699b8dbd1f773f442d8'
url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=alerts&appid={api_key}&units=metric&cnt=12'
data = requests.get(url).json()

#current weather information
current_weather_description = data['current']['weather'][0]['description']
current_temperature = data['current']['temp']
current_wind_deg = data['current']['wind_deg']
current_wind_speed = data['current']['wind_speed']

#hourly temperature
from datetime import datetime
hourly = data['hourly']
hourly_temperature = {}
for entry in hourly:
    dt_object = datetime.fromtimestamp(entry['dt'])
    hourly_temperature[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')] = entry['temp'] 

#daily temperature
daily = data['daily']
daily_temperature = {}
for entry in daily:
    dt_object = datetime.fromtimestamp(entry['dt'])
    daily_temperature[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')] = [entry['temp']['day'], entry['temp']['min'], entry['temp']['max'], entry['temp']['night'], entry['temp']['morn']]

#minutely precipitation
minutely = data['minutely']
minutely_precipitation = {}
for entry in minutely:
    dt_object = datetime.fromtimestamp(entry['dt'])
    minutely_precipitation[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')] = entry['precipitation']

#daily wind direction
daily = data['daily']
daily_wind_deg = {}
for entry in daily:
    dt_object = datetime.fromtimestamp(entry['dt'])
    daily_wind_deg[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')] = entry['wind_deg']

#daily wind speed
daily = data['daily']
daily_wind_speed = {}
for entry in daily:
    dt_object = datetime.fromtimestamp(entry['dt'])
    daily_wind_speed[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')] = entry['wind_speed']



st.write(f"Current City: {captured_address}")
st.write("Current weather description: " + current_weather_description)
st.write(f"Current temperature: {current_temperature}°C")
st.write("Wind speed:")
st.bar_chart(daily_plot_wind(daily_wind_speed))


st.write("___________________")



# st.write("""Address
#         #Titel
#         Eingabe und Anzeige Stadtname
#         Aktuelle Daten
#         2 Columns: Temp-Plots links, Nds-Pltos rechts mit je Schaltfläche welcher Plot gezeigt werden soll
#         Weltkarte         
#""")


st.line_chart(hourly_plot_temp(hourly_temperature))
st.line_chart(daily_plot_temp(daily_temperature))


