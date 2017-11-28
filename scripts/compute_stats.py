#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 21:54:12 2017

@author: isaacmehigan
"""

#Test creation of dataframe


import pandas as pd
import statistics as stat
import datetime

def compute_stats(df):
    days=[]
    mean_mag_JJY=[]
    disp_mag_JJY=[]
    mean_phase_JJY=[]
    disp_phase_JJY=[]
    DFList = []
    for group in df.groupby(df.index.day):
        DFList.append(group[1])
    for day in DFList:
        days.append(day.index[0].date())
        mean_mag_JJY.append(stat.mean(day['A_jjy']))
        mean_phase_JJY.append(stat.mean(day['P_jjy']))
        disp_mag_JJY.append(stat.pvariance(day['A_jjy']))
        disp_phase_JJY.append(stat.pvariance(day['P_jjy']))
    d={'mean_mag_JJY': mean_mag_JJY,'mean_phase_JJY': mean_phase_JJY,
       'disp_mag_JJY': disp_mag_JJY,'disp_phase_JJY': disp_phase_JJY}
    stats_df=pd.DataFrame(data=d,index=days)
    return stats_df
#collumn_names=[['M_nwc','D_nwc','M_npm','D_npm','M_jji','D_jji','M_jjy','D_jjy']]

stats_df=compute_stats(All_night_data) #Uses DF already in the workspace from main.py
