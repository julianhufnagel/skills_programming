##########################################################################
# WeatherApp                                                             #
#                                                                        #
# created by Julian Hufnagel, Janina Moser, Elena Fecher & Deniz Harimci #
# in the course "Introduction into Programming" with Mario Silic         #
# requirements and credits are mentioned in readme.txt                   #
#                                                                        #
##########################################################################


#############################################
# library imports
#############################################

import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json
import geopy
from geopy.geocoders import Nominatim
import geocoder
import requests
import datapackage
from PIL import Image


#############################################
# Access Keys
#############################################

px.set_mapbox_access_token('pk.eyJ1IjoiZGVubmlzc2lvIiwiYSI6ImNrbXg4NjhvZDBtOHkyb24xd3p5anE3NWYifQ.2U5ETPfl1WL1aGZFy5DZmA') #plotly
api_key = 'aad6e7a0184b7699b8dbd1f773f442d8' #openweathermap


#############################################
# Load
#############################################

data_cities =  pd.read_csv('data/world-cities_csv.csv')


#############################################
# styling
#
# adapting streamlit layout 
# -> changing footer &  Menu
#############################################

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


#############################################
# Set location
#############################################

geolocator = Nominatim(user_agent="WeatherApp") 
g = geocoder.ip('me') #access destination via IP
address = st.text_input("Please enter a city name", g.city) #input field for destination default from IP
location = geolocator.geocode(address, language='en')
#error handling, if city is not known
try:
    lat = location.latitude
    lon = location.longitude
except:
    st.error("This city is not known to our system. Please try another city.")
    st.stop()
reverse_loc = geolocator.reverse(f"{lat},{lon}", language='en')
country_finder = reverse_loc.raw['address']
country = country_finder.get('country', '') #find country of specified city


#############################################
# Data import from destination
#############################################

url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=alerts&appid={api_key}&units=metric&cnt=12'
data = requests.get(url).json()

#access current weather information
current_weather_description = data['current']['weather'][0]['description']
current_weather_icon = data['current']['weather'][0]['icon']
current_temperature = data['current']['temp']
current_wind_deg = data['current']['wind_deg']
current_wind_speed = data['current']['wind_speed']

#access single entries within hourly temperature
from datetime import datetime
hourly = data['hourly']
hourly_temperature = {}
for entry in hourly:
    dt_object = datetime.fromtimestamp(entry['dt'])
    hourly_temperature[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')] = entry['temp'] 

#access single entries within daily temperature
daily = data['daily']
daily_temperature = {}
for entry in daily:
    dt_object = datetime.fromtimestamp(entry['dt'])
    daily_temperature[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')] = [entry['temp']['day'], entry['temp']['min'], entry['temp']['max'], entry['temp']['night'], entry['temp']['morn']]

#access single entries within minutely precipitation
minutely = data['minutely']
minutely_precipitation = {}
for entry in minutely:
    dt_object = datetime.fromtimestamp(entry['dt'])
    minutely_precipitation[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')] = entry['precipitation']
        
#access rain volume for last hour in mm
current_rain = data['current']
for entry in current_rain:
    if 'rain' in entry:
        current_rain_1h = data['current']['rain']['1h']
    else:
        current_rain_1h = 0
        
#access rain volume hourly in mm
hourly = data['hourly']
hourly_rain = {}
for entry in hourly:
        if 'rain' in entry:
                dt_object = datetime.fromtimestamp(entry['dt'])
                hourly_rain[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')] = entry['rain']['1h']
        else:
                hourly_rain = 0

#access daily precipitation volume in mm
daily = data['daily']
daily_rain = {}
for entry in daily:
        if 'rain' in entry:
                dt_object = datetime.fromtimestamp(entry['dt'])
                daily_rain[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')] = entry['rain']
        else:
                daily_rain = 0

#access single entries within daily wind direction
daily = data['daily']
daily_wind_deg = {}
for entry in daily:
    dt_object = datetime.fromtimestamp(entry['dt'])
    daily_wind_deg[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')] = entry['wind_deg']

#access single entries within daily wind speed
daily = data['daily']
daily_wind_speed = {}
for entry in daily:
    dt_object = datetime.fromtimestamp(entry['dt'])
    daily_wind_speed[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')] = entry['wind_speed']


#############################################
# Functions
#############################################

def daily_plot_temp(daily_temperature):
    #'''define callable function 
    # for daily temperature with 
    # variables from the API'''
    df = pd.DataFrame(list(daily_temperature.items()),columns = ['Date','Temperature']) #gathered data from dict into Dataframe
    df[['day','min','max','night','morn']] = pd.DataFrame(df['Temperature'].to_list(), columns=['day','min', 'max', 'night', 'morn']) #split the data stored in the temperature list into individual columns
    del df['Temperature'] #delete column with unnecessary information
    df = df.set_index("Date")[["day","min","max"]] #select to plot min, max and day temperature in a diagramm (three lines)
    cnt = st.slider('Select how many days of prediction you want', min_value=3, max_value=7) #slider that allows to change the length of the prediction
    return df.iloc[0:cnt,0:3]

def hourly_plot_temp(hourly_temperature):
    #'''define callable function requiring
    #  hourly temperature from the
    #  openweathermap API'''
    df = pd.DataFrame(list(hourly_temperature.items()),columns = ['Date/Time','Temperature']) #dictionary into dataframe
    df = df.set_index("Date/Time") #set up data for plot
    return df

def daily_plot_wind(daily_wind_speed):
    #'''define callable function requiring
    #  daily wind speed from the
    #  openweathermap API'''
    df = pd.DataFrame(list(daily_wind_speed.items()),columns = ['Date/Time','Windspeed']) #dictionary into dataframe
    df = df.set_index("Date/Time") #set up data for bar plot
    return df

def find_countries(countries):
    #'''callable function 
    #  to matched searched country 
    #  with dataset'''
    result = data_cities.loc[data_cities['country'] == f'{countries}']
    return result

def find_subcountries():
    #'''find all subcountries
    #  in the given country'''
    our_country = find_countries(country)
    unique_subcountry = our_country.drop_duplicates(subset ="subcountry",keep = "first")
    list_subcountries = unique_subcountry["name"].to_numpy() #make list without duplicates
    return list_subcountries

def store_temperature():
    #'''function preparing data 
    # for the map with dest, 
    # lat, lon, temp'''
    list_destinations = find_subcountries()
    dict_map = {"dest": [], "lat": [], "lon": [], "temp": []} #empty dict to append data from desitnations
    for i in range(0,len(list_destinations)):
        j = list_destinations[i]
        destination = geolocator.geocode(j)
        if destination == None: #avoiding errors from not found destination
            pass
        else:
            dest_lat = destination.latitude
            dest_lon = destination.longitude
            api_key = 'aad6e7a0184b7699b8dbd1f773f442d8'
            url = f'https://api.openweathermap.org/data/2.5/onecall?lat={dest_lat}&lon={dest_lon}&exclude=alerts&appid={api_key}&units=metric&cnt=12'
            weather_data = requests.get(url).json()
            temp = weather_data['current']['temp']
            #append weather data to dict
            dict_map['dest'].append(j)
            dict_map['lat'].append(dest_lat)
            dict_map['lon'].append(dest_lon)
            dict_map['temp'].append(temp)
    return dict_map

def map_temperature():
    #'''function 
    map_data = store_temperature()
    df = pd.DataFrame.from_dict(map_data, orient='columns')
    if df.empty == True:
        st.error('Unfortunately, we can not find your country in our database')
    else:
        fig = px.scatter_mapbox(df, hover_data=['temp', 'dest'], lat='lat', lon='lon',
                                    color='temp',
                                    color_continuous_scale=px.colors.sequential.Sunsetdark)
        fig.update_layout(
        mapbox_style="mapbox://styles/dennissio/ckmx8cxq00l0317nslyw06i0m")
        fig.update_mapboxes(center_lon = lon, center_lat = lat, zoom = 6)
        st.plotly_chart(fig)
    

#############################################
# Frontend Layout
#############################################


st.button('Search')
st.write(f"Current City: {location}")
st.write("Current weather description: " + current_weather_description)
url_img = f"images/{current_weather_icon}.png"
st.image(Image.open(url_img))
st.write(f"Current temperature: {current_temperature}°C")
st.write("Wind speed:")
st.bar_chart(daily_plot_wind(daily_wind_speed))
st.write("___________________")
st.area_chart(hourly_plot_temp(hourly_temperature))
st.line_chart(daily_plot_temp(daily_temperature))
map_temperature()


# st.write("""Address
#         #Titel
#         Eingabe und Anzeige Stadtname
#         Aktuelle Daten
#         2 Columns: Temp-Plots links, Nds-Pltos rechts mit je Schaltfläche welcher Plot gezeigt werden soll
#         Weltkarte         
#""")


