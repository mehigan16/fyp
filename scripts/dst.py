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

Fixed initial issue with a find "(\d)-" and replace "\1 -"


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
#    d={'num':range(0,length,1)}
#    d=pd.Series()
#    df=df.fillna(-50)
#    df=df.fillna(method='pad', limit=1)

#    df2=pd.DataFrame(data=d, index=rng, columns=None, dtype=None, copy=False)
    for y in range(0,len(df.index)):
        tmp_list=df.iloc[y][3:27].tolist()
        day_values=[]
        for value in tmp_list:
            day_values.append(value)
#            if type(value) is str:
#                if 'n' in value:
#                    continue  
#                if len(value.split('-')) > 2:
#                    for entry in value.split('-')[1:]:
#                        entry='-'+entry
#                        day_values.append(entry)
#    #                values.append(-100)
#                else:
#                    day_values.append(value)
##            elif value==999:
##                continue
#            else:
#                day_values.append(value)
#        if len(day_values) is 26:
#            day_values.pop()
##            print("bad")
#        if len(day_values) is not 25: 
#            print(day_values)
        values.extend(day_values)        
    df2=pd.DataFrame(data=values, index=rng, columns=["dst"], dtype=None, copy=False)
    
#    df2['dst']=values
#    df3=df2.between_time('18:00','8:00')
#    df4=df2.fillna(999)
#    df5=fix_string_values(df4)
    return df2

def load(file):
    """ Function to load the dst data into a dataframe
    """
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
    return dst_data

def fix_string_values(df):
    """ Function to take the raw non strings and convert to -100 value
    Note: there were 16 in the 2004-2007 data
    """
    values=[]
    for value in df['dst_raw']:
        if type(value) is str:
#            if 'n' in value:
#                continue  
            if len(value.split('-')) > 2:
                for entry in value.split('-')[1:]:
                    entry='-'+entry
                    values.append(entry)
#                values.append(-100)
            else:
                values.append(value)
        elif value==999:
            continue
        else:
            values.append(value)
    df['dst']=values
    df['dst']=pd.to_numeric(df['dst'])
    return df
def find_under_threshold(threshold):
    print("not yet done")

def test_date(df,date,*threshold):
    """ Function to check if the dst value was below the threshold on the
    24 hours around the given datetime. threshold is -50 if nothing given.
    """
    lower_date=date-datetime.timedelta(hours=12)
    upper_date=date+datetime.timedelta(hours=12)
    exact_value=df.loc[date].dst
    values=df.loc[lower_date:upper_date].dst
    minimum=values.min()
    average=values.mean()
    if not threshold:
        threshold = -50
    else:
        threshold=threshold[0]
    if minimum > threshold:
        return 1
    elif (exact_value > threshold and average > threshold):
        print("Warning 1 value in the 24hr range was below threshold")
        return 1
    else:
        return 0
#------------------------------------------------------------
file="dst_2004-01-01_2007-12-31-fixed.dat"
colNames=['DST_name','Version','Base_value','1','2','3','4','5','6','7','8','9','10',
          '11','12','13','14','15','16','17','18','19','20','21','22','23','24','avg']

dst_data=load(file)
dst_df=condition(dst_data)
#df[df['A'] < -1.0].index.tolist()
#over20=dst_df[dst_df['dst']>20].index.tolist()