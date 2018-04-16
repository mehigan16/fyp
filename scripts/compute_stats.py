#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 21:54:12 2017

A module to compute the stats for the mean and displacement of the JJY
amplitude and phase signals
@author: isaacmehigan
"""

import pandas as pd
import statistics as stat
import numpy as np

def compute_stats(df):
    days=[]
    mean_mag_JJY=[]
    disp_mag_JJY=[]
    mean_phase_JJY=[]
    disp_phase_JJY=[]
    DFList = []
#    df['A_jjy']=df['A_jjy'].replace(to_replace=0, method='ffill',limit=180).values #Forward fill 0 values
#    df['P_jjy']=df['P_jjy'].replace(to_replace=0, method='ffill',limit=180).values #Forward fill 0 values
    for group in df.groupby(df.index.date):
        DFList.append(group[1])
    for day in DFList:
        days.append(day.index[0].date())
        day.astype(bool).sum(axis=0)
        A_zeros=day.shape[0]-day['A_jjy'].astype(bool).sum(axis=0)
        P_zeros=day.shape[0]-day['P_jjy'].astype(bool).sum(axis=0)
        if (A_zeros > 360 or P_zeros > 360):
            mean_mag_JJY.append(np.nan)
            mean_phase_JJY.append(np.nan)
            disp_mag_JJY.append(np.nan)
            disp_phase_JJY.append(np.nan)
        else:
            mean_mag_JJY.append(stat.mean(day['A_jjy']))
            mean_phase_JJY.append(stat.mean(day['P_jjy']))
            disp_mag_JJY.append(stat.pvariance(day['A_jjy']))
            disp_phase_JJY.append(stat.pvariance(day['P_jjy']))
    d={'mean_mag_JJY': mean_mag_JJY,'mean_phase_JJY': mean_phase_JJY,
       'disp_mag_JJY': disp_mag_JJY,'disp_phase_JJY': disp_phase_JJY}
    stats_df=pd.DataFrame(data=d,index=days)
#    stats_df=stats_df.drop(stats_df.index[0]) #Drop first row as only 3 sampls
    return stats_df


def select_values(df,eq_list):
    for index, eq in eq_df.iterrows():    
        eq_date=datetime.datetime(index.year,index.month,index.day)
        date1=eq_date - datetime.timedelta(days=10)
        candidate_df=df[date1:eq_date]
        if candidate_df.shape[0] == 5:
            



df=pd.read_hdf("/Users/isaacmehigan/Documents/fyp/kam/h5/2004-02-15_2007-12-30.h5")
df=df[['A_jjy','P_jjy']]

dst_df=pd.read_hdf("/Users/isaacmehigan/Documents/fyp/h5/dst.h5")
dst_df=dst_df.loc['2004-2-15':'2007-12-30'] # Only takes days after 18th feb (5 days after data begins) 
eq_df=pd.read_hdf("/Users/isaacmehigan/Documents/fyp/h5/eq.h5")
eq_df=eq_df.loc['2004-2-15':'2007-12-30']


df_Stat2=compute_stats(df)

dst_mins=dst_df.resample('D')['dst'].agg(['min'])
df_Stat2['dst']=dst_mins['min'].values

df_Stat2.to_hdf("/Users/isaacmehigan/Documents/fyp/h5/mean_disp_dst.h5",'stats_df',format='table')
df_Stat3=df_Stat2[df_Stat2['dst']>-50]