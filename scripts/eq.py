#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:13:07 2017

Module to load and process the eq list data

@author: isaacmehigan
"""

import os
import datetime
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def load(file):
    """ Function to Load list of earthquakes """
    file_name="../eq_lists/"+file
    data = pd.read_csv(file_name,
                       sep=',', 
                       engine='python',
                       verbose=True,
                       header='infer'
                       )
    return data

def convert_date_time(df):
    """ Function to add the timestamp for the file as the index col
    """
    tmp=df.index
    rng=[]
#    2004-01-11T19:31:32.820Z
    df_format='%Y-%m-%dT%H:%M:%S.%fZ'
    for eq in df['time']:
        dt=datetime.datetime.strptime(eq,df_format)
        rng.append(dt)
#    start_date=start_date-datetime.timedelta(minutes=1)
#    rng=pd.date_range(start_date,freq='20s',periods=length)
    df['time']=rng
#    df['num']=tmp
    df2=df.set_index('time')
    return df2

def get_marker_color(magnitude):
    """ Function to change marker size and colour for the plotting of eqs based 
    on the magnitude of the eq"""
    if magnitude < 6.0:
        return ('go'),6
    elif magnitude < 6.5:
        return ('yo'),8
    else:
        return ('ro'),10

def check_valid(eq,distance_threshold):
    """ Function to check if the earthquake would have been registered along the
    transmission path
    """
    # Transmitter and reciever lat and longitudes
    tLong=140.849007
    tLat=37.372557
    rLong=158.92
    rLat=53.15
    if eq.latitude > rLat:
        return -1
    elif eq.latitude<tLat:
        return -1
    if eq.longitude>rLong:
        return -1
    elif eq.longitude<tLong:
        return -1   
    v=[rLong-tLong, -(rLat-tLat)] # Point A is [x1,y1] Point B is [x2,y2]
    u=[tLong-eq.longitude, tLat-eq.latitude]
    distance = abs( (rLong-tLong)*(tLat-eq.latitude) - (tLong-eq.longitude)*(rLat-tLat) )
    if distance > distance_threshold:
        return -1*distance
    else:
        return distance

def proccess_eqs(df,distance_threshold):
    """ Function to delete irrellevant earthquakes """
    markers=[]
    sizes=[]
    for index, row in df.iterrows():
            dist=check_valid(row,distance_threshold)
            if dist<0:
                df=df.drop(index)
            else:
                [m,s] = get_marker_color(row.mag)
                markers.append(m)
                sizes.append(s)
    df['marker']=markers
    df['marker_size']=sizes
    return df
    


def plot(df):
    """ Function to plot the eqs on the line of the transmitter reciever """
    
    # Transmitter and reciever lat and longitudes
    tLong=140.849007
    tLat=37.372557
    rLong=158.92
    rLat=53.15
    
    map = Basemap(projection='merc', #lat_0 = 40, lon_0 = 140,
              resolution = 'i', #area_thresh = 0.1,
              llcrnrlon=135, llcrnrlat=36,
              urcrnrlon=165, urcrnrlat=55)
    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color = 'gray')  #coral
    map.drawmapboundary()


    linex,liney = map([tLong,rLong],[tLat, rLat])
    map.plot(linex,liney,'m')
    map.plot(linex,liney,'m*',markersize=15)
    
    lons = df.longitude.tolist()
    lats = df.latitude.tolist()
    x,y = map(lons, lats)
    
    df['x']=x
    df['y']=y
    
#    data2=data
    
    for index, row in df.iterrows():         
        map.plot(row.x, row.y, row.marker , markersize=row.marker_size )

    plt.show()



# Section for testing the functions within the file.
distance_threshold=50

df=load("2004_2007_eqs.csv")

df=convert_date_time(df)

df2=proccess_eqs(df,distance_threshold)
plot(df2)
