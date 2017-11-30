#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:43:30 2017
This file is to load the dst data
@author: isaacmehigan
"""

"""
Taken from: http://wdc.kugi.kyoto-u.ac.jp/dstae/index.html

RECORD FORMAT (LENGTH: 120 BYTE FIXED)
COLUMN	FORMAT	SHORT DESCRIPTION
1-3	A3	Index name 'DST'
4-5	I2	The last two digits of the year
6-7	I2	Month
8	A1	'*' for index
9-10	I2	Date
11-12	A2	All spaces or may be "RR" for quick look
13	A1	'X' (for index)
14	A1	Version (0: quicklook, 1: provisional, 2: final, 3 and up: corrected final or may be space)
15-16	I2	Top two digits of the year (19 or space for 19XX, 20 from 2000)
17-20	I4	Base value, unit 100 nT
21-116	24I4	24 hourly values, 4 digit number, unit 1 nT, value 9999 for the missing data.
First data is for the first hour of the day, and Last data is for the last hour of the day.
117-120	I4	Daily mean value, unit 1 nT. Value 9999 for the missing data.

"""

import pandas as pd

import plotly.plotly as py
import plotly.graph_objs as go
import datetime

#Functions--------------------------------------------------

def add_date_col(df):
    """ Function to add the timestamp for the file as the index col
    """
    date_format='DST%y%m*%d'
    start_date=datetime.datetime.strptime(df.iloc[0][0],date_format)
    length=len(df.index)
    tmp=df.index
    rng=pd.date_range(start_date,freq='1d',periods=length)
    df['time']=rng
    df['num']=tmp
    df2=df.set_index('time')
    return df2

def condition(df):  
    """ Function to condition the dst data to remove non values and to make
    a long list of data for each hour slot at night
    """
    values=[]
    start_date=df.index[0]
    length=len(df.index)*24
    rng=pd.date_range(start_date,freq='1h',periods=length)
    d={'num':range(0,length,1)}
#    d=pd.Series()
#    df=df.fillna(-50)
#    df=df.fillna(method='pad', limit=1)

    df2=pd.DataFrame(data=d, index=rng, columns=None, dtype=None, copy=False)
    for y in range(0,len(df.index)):
        for value in df.iloc[y][3:27].tolist():
            values.append(value)        
    df2['dst']=values
    df3=df2.between_time('18:00','8:00')
    return df3.fillna(-100)

def add_dst_index(data,filename):
    split=filename.split('-')
    start_date=datetime.datetime(int(split[1]),int(split[2]),int(split[3]))
    tmp=data.index
    length=len(tmp)
    rng=pd.date_range(start_date,freq='1d',periods=length)
    data['time']=rng
    data['num']=tmp
    data2=data.set_index('time')
    return data2

#------------------------------------------------------------
file="dst_2004-01-01_2007-12-31.dat"
colNames=['DST_name','Version','Base_value','1','2','3','4','5','6','7','8','9','10',
          '11','12','13','14','15','16','17','18','19','20','21','22','23','24','avg']


dst_data = pd.read_csv("../dst/"+file,
                       sep='\s+', 
                       engine='python',
                       index_col=False,
                       names=colNames,
                       header=None,
                       skiprows=0
                       )

dst_data=add_date_col(dst_data)

def to_unix_time(dt):
    epoch =  datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000


