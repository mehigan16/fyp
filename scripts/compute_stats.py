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
import datetime
from random import randint


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
        days.append(day.index[0])
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
    df['eq']=np.zeros(df.shape[0])
    df['taken']=np.zeros(df.shape[0])
    result_array=np.zeros(21)
    earthquake_dates=[]
    for index, eq in eq_df.iterrows():    
        eq_date=datetime.date(index.year,index.month,index.day)
        date1=eq_date - datetime.timedelta(days=5)
        candidate_df=df[date1:eq_date-datetime.timedelta(days=1)]
        if (candidate_df.shape[0] == 5 and candidate_df[candidate_df['dst']>-50].shape[0]==5 and candidate_df['mean_mag_JJY'].isnull().sum()<1 and candidate_df['taken'].sum()<1):
            candidate_df=candidate_df.drop(['dst', 'eq','taken'], axis=1)
            stats_list=candidate_df.values.flatten()[0:20]
            stats_list=np.hstack((stats_list,1)) # Add target data
            result_array = np.vstack((result_array, stats_list))
            df.loc[date1:eq_date+datetime.timedelta(days=6), 'eq'] = 1
            df.loc[date1:eq_date, 'taken'] = 1
    
# =============================================================================
#     Now for control
# =============================================================================
    i=0
    max_r=df.shape[0]-1    
    num_eqs=result_array.shape[0]-1
    while (i< num_eqs):
        r=randint(5,max_r)
        date2=df.index[r].date()
        date1=df.index[r-6].date()
        candidate_ctrl=df[date1:date2]
        if (candidate_ctrl.shape[0] == 7 and candidate_ctrl[candidate_ctrl['dst']>-50].shape[0]==7 and candidate_ctrl['mean_mag_JJY'].isnull().sum()<1 and candidate_ctrl['eq'].sum()<1):
            candidate_ctrl=candidate_ctrl.drop(['dst', 'eq','taken'], axis=1)
            stats_list=candidate_ctrl.values.flatten()[0:20]
            stats_list=np.hstack((stats_list,0)) # Add target data
            result_array = np.vstack((result_array, stats_list))
            df.loc[date1:date2, 'eq'] = 1
            i=i+1
            print(i)
    result_array=result_array[1:,:]
    return df,result_array

output_dir="/Users/isaacmehigan/Documents/fyp/training_datasets/"
df=pd.read_hdf("/Users/isaacmehigan/Documents/fyp/kam/h5/2004-02-15_2007-12-30.h5")
df=df[['A_jjy','P_jjy']]

dst_df=pd.read_hdf("/Users/isaacmehigan/Documents/fyp/h5/dst.h5")
dst_df=dst_df.loc['2004-2-15':'2007-12-30'] # Only takes days after 18th feb (5 days after data begins) 
eq_df=pd.read_hdf("/Users/isaacmehigan/Documents/fyp/h5/eq.h5")
eq_df=eq_df.loc['2004-2-24':'2007-12-30']
df_Stat2=pd.read_hdf("/Users/isaacmehigan/Documents/fyp/h5/mean_disp_dst.h5")



df,D=select_values(df_Stat2,eq_df)
#np.savetxt(output_dir+"earthquake_data-corrected.csv", D, delimiter=",")
#df_Stat2=compute_stats(df)



#dst_mins=dst_df.resample('D')['dst'].agg(['min'])
#df_Stat2['dst']=dst_mins['min'].values

#df_Stat2.to_hdf("/Users/isaacmehigan/Documents/fyp/h5/mean_disp_dst.h5",'stats_df',format='table')
#df_Stat3=df_Stat2[df_Stat2['dst']>-50]