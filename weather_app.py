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
from datetime import datetime
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

#############################################
# Access Keys
#############################################

px.set_mapbox_access_token('pk.eyJ1IjoiZGVubmlzc2lvIiwiYSI6ImNrbXg4NjhvZDBtOHkyb24xd3p5anE3NWYifQ.2U5ETPfl1WL1aGZFy5DZmA') #plotly api key
api_key = 'aad6e7a0184b7699b8dbd1f773f442d8' #openweathermap api key


#############################################
# Load
#############################################

data_cities = pd.read_csv("https://raw.githubusercontent.com/julianhufnagel/skills_programming/main/data/world-cities_csv.csv")

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
st.image("https://raw.githubusercontent.com/julianhufnagel/skills_programming/main/images/Weatherapp.png")

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
hourly = data['hourly']
hourly_temperature = {}
for entry in hourly:
    hourly_temperature[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')] = entry['temp'] 

#access single entries within daily temperature
daily = data['daily']
daily_temperature = {}
for entry in daily:
    daily_temperature[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')] = [entry['temp']['day'], entry['temp']['min'], entry['temp']['max'], entry['temp']['night'], entry['temp']['morn']]

#access single entries within minutely precipitation
minutely = data['minutely']
minutely_precipitation = {}
for entry in minutely:
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
                hourly_rain[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')] = [entry['rain']['1h'], entry['pop']]
        else:
                hourly_rain[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')] = [0, entry['pop']]

#access daily precipitation volume in mm
daily = data['daily']
daily_rain = {}
for entry in daily:
        if 'rain' in entry:
                daily_rain[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')] = [entry['rain'], entry['pop']]
        else:
                daily_rain[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')] = [0, entry['pop']]

#access single entries within daily wind direction
daily = data['daily']
daily_wind_deg = {}
for entry in daily:
    daily_wind_deg[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')] = entry['wind_deg']

#access single entries within daily wind speed
daily = data['daily']
daily_wind_speed = {}
for entry in daily:
    daily_wind_speed[datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')] = entry['wind_speed']


#############################################
# Functions
#############################################

def daily_plot_temp():
    #'''define callable function 
    # for daily temperature with 
    # variables from the API'''
    df = pd.DataFrame(list(daily_temperature.items()),columns = ['Date','Temperature']) #gathered data from dict into Dataframe
    df[['day','min','max','night','morn']] = pd.DataFrame(df['Temperature'].to_list(), columns=['day','min', 'max', 'night', 'morn']) #split the data stored in the temperature list into individual columns
    del df['Temperature'] #delete column with unnecessary information
    cnt = st.slider('Select how many days of prediction you want', min_value=3, max_value=7) #slider that allows to change the length of the prediction
    fig = go.Figure()
    fig.add_traces(go.Scatter(x=df.iloc[0:cnt,:]['Date'], y=df.iloc[0:cnt,:]['day'], mode='lines', name = 'daily mean', line=dict(color='green', width=2)))
    fig.add_traces(go.Scatter(x=df.iloc[0:cnt,:]['Date'], y=df.iloc[0:cnt,:]['min'], mode='lines', name = 'daily min', line=dict(color='blue', width=2)))
    fig.add_traces(go.Scatter(x=df.iloc[0:cnt,:]['Date'], y=df.iloc[0:cnt,:]['max'], mode='lines', name = 'daily max', line=dict(color='red', width=2)))
    #df.iloc[0:cnt,0:3], x = 'Date', y =  px.line(df, x= 'Date', y = 'Temperature', title="Daily temperature prediction")
    #fig.add_trace(x=df.iloc[0:cnt,:]['Date'], y=df.iloc[0:cnt,:]['min'], mode='lines')
    #fig.add_trace(x=df.iloc[0:cnt,:]['Date'], y=df.iloc[0:cnt,:]['max'], mode='lines')
    return fig

def hourly_plot_temp():
    #'''define callable function requiring
    #  hourly temperature from the
    #  openweathermap API'''
    df = pd.DataFrame(list(hourly_temperature.items()),columns = ['Date/Time','Temperature']) #dictionary into dataframe
    fig = px.line(df, x='Date/Time', y='Temperature',
             labels={'Temperature':'Temperature in ??C'})
    return fig

def daily_plot_wind():
    #'''define callable function requiring
    #  daily wind speed from the
    #  openweathermap API'''
    df = pd.DataFrame(list(daily_wind_speed.items()),columns = ['Date','Windspeed']) #dictionary into dataframe
    fig = px.bar(df, x ='Date', y = 'Windspeed')
    return fig

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
    unique_subcountry = our_country.drop_duplicates(subset ="subcountry",keep = "first") #only keep values once
    list_subcountries = unique_subcountry["name"].to_numpy() #make list without duplicates
    return list_subcountries

def store_temperature():
    #'''function preparing data 
    # for the map with dest, 
    # lat, lon, temp'''
    list_destinations = find_subcountries()
    dict_map = {"dest": [], "lat": [], "lon": [], "temp": [], "rain": []} #empty dict to append data from desitnations
    for i in range(0,len(list_destinations)): #loop through entire list
        j = list_destinations[i]
        destination = geolocator.geocode(j)
        if destination == None: #avoiding errors from not found destination
            pass
        else:
            dest_lat = destination.latitude
            dest_lon = destination.longitude
            api_key = 'aad6e7a0184b7699b8dbd1f773f442d8' #key for openweatherman
            url = f'https://api.openweathermap.org/data/2.5/onecall?lat={dest_lat}&lon={dest_lon}&exclude=alerts&appid={api_key}&units=metric&cnt=12'
            weather_data = requests.get(url).json() #assign json response
            temp = weather_data['current']['temp']
            rain = weather_data['current']
            if 'rain' in rain: #check rain if given
                current_rain1h = weather_data['current']['rain']['1h']
            else:
                current_rain1h = 0
            #append weather data to dict
            dict_map['dest'].append(j)
            dict_map['lat'].append(dest_lat)
            dict_map['lon'].append(dest_lon)
            dict_map['temp'].append(temp)
            dict_map['rain'].append(current_rain1h)
    return dict_map

def map_weather():
    #'''function to illustrate data
    #  on map'''
    map_data = store_temperature() #call function to access data
    df = pd.DataFrame.from_dict(map_data, orient='columns') #dict to Dataframe
    if df.empty == True: #error handling 
        st.error('Unfortunately, we can not find your country in our database')

    else: #information plotted on a map
        fig = px.scatter_mapbox(df, hover_data=['dest', 'temp', 'rain'], lat='lat', lon='lon',
                                    color='temp',
                                    color_continuous_scale=px.colors.sequential.Sunsetdark)
        fig.update_layout(
        mapbox_style="mapbox://styles/dennissio/ckmx8cxq00l0317nslyw06i0m") #select map style
        fig.update_mapboxes(center_lon = lon, center_lat = lat, zoom = 6) #set initial zoom
    return fig
   
        
def hourly_plot_rainvolume():
    #'''define callable function requiring
    #  hourly rain volume from the
    #  openweathermap API'''
    df = pd.DataFrame(list(hourly_rain.items()),columns = ['Date/Time','Rain Volume']) #dictionary into dataframe
    df[['rain', 'pop']] = pd.DataFrame(df['Rain Volume'].to_list(), columns=['rain', 'pop']) #split the data stored into individual columns
    del df['Rain Volume'] #delete column with unnecessary information
    fig = px.bar(df, x='Date/Time', y='rain',
             hover_data=['pop'],
             labels={'rain':'Rain in mm'})
    return fig

def daily_plot_precipitation():
    #'''define callable function requiring
    #  daily precipitation from the
    #  openweathermap API'''
    df = pd.DataFrame(list(daily_rain.items()),columns = ['Date/Time','Precipitation']) #dictionary into dataframe
    df[['prec', 'pop']] = pd.DataFrame(df['Precipitation'].to_list(), columns=['prec', 'pop']) #split the data stored into individual columns
    del df['Precipitation'] #delete column with unnecessary information
    fig = px.bar(df, x='Date/Time', y='prec',
             hover_data=['pop'],
             labels={'prec':'Rain in mm'})
    return fig
  

#############################################
# Frontend Layout
#############################################

col1_1, col2_1 = st.beta_columns([1, 3])    
with col1_1:
    st.button('Search')
with col2_1:
    st.write(f"Current City: {location}")    
st.header("How is the weather now?")
col1_2, col2_2 = st.beta_columns([1, 3])
with col1_2:
    st.image(f"https://raw.githubusercontent.com/julianhufnagel/skills_programming/main/images/{current_weather_icon}.png")
with col2_2:
    st.write(f"The weather is currently {current_weather_description} with {current_temperature}??C")
    
with st.form(key='next_hours'):    
    st.write("And how will it be within")
    col1_3, col2_3 = st.beta_columns([1, 1])
    with col1_3:
        submit_button_hours = st.form_submit_button(label='in the next hours?')
    with col2_3:
        submit_button_days = st.form_submit_button(label='in the next days?')
    
if submit_button_hours:
    st.header("Temperatur and rainvolume for the next hours")
    st.subheader("Temperature")
    st.plotly_chart(hourly_plot_temp())
    st.subheader("Rainvolume")
    st.plotly_chart(hourly_plot_rainvolume())
    
if submit_button_days:
    st.header("Temperatur and rainvolume for the next days")
    st.subheader("Temperature")
    st.plotly_chart(daily_plot_temp())
    st.subheader("Rainvolume")
    st.plotly_chart(daily_plot_precipitation())
    
    
st.write("___________________")

with st.form(key='wind'):
    st.write("In case you care about wind, click here")
    submit_button_wind = st.form_submit_button(label='I care about wind')

if submit_button_wind:
    st.subheader("Wind for the next days")
    st.plotly_chart(daily_plot_wind())
    
with st.form(key='map'):
    st.write("Wanna see a cool heat map?")
    submit_button_map = st.form_submit_button(label='Yes I do')

if submit_button_map:
    st.header("Heat Map")
    st.plotly_chart(map_weather())
