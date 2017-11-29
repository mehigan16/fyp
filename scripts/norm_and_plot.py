#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 00:09:54 2017

@author: isaacmehigan
"""

#Normalize all the values in a dataframe, keeping col names and index
#Plot a bar chart and a line chart of the dataframe for comparison

from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt

def norm_df(df):
    x = df.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    index=df.index
    column_headers=list(df)
    df = pd.DataFrame(x_scaled,columns=column_headers,index=index)
    return df

def plot_stat_df(df):
    df.plot.bar()
    df.plot()
    