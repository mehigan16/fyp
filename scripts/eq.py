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

def load(file):
    
    file_name="../eq_lists/"+file
    data = pd.read_csv(file_name,
                       sep=',', 
                       engine='python',
                       verbose=True,
                       header='infer'
                       )
    return data

def index_date_time(df):
    """ Function to add the timestamp for the file as the index col
    """
    length=len(df.index)
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
    df['num']=tmp
    #df2=df.set_index('datetime')
    return df

df=load("2004_eqs.csv")

df2=index_date_time(df)