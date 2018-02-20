#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:30:38 2018

@author: isaacmehigan

Pre-modelling

"""


import dst as dst
import vlf as vlf
#import eq as eq
import compute_stats as cs
import os
import pandas as pd
import datetime
import statistics as stat
import numpy as np

def load():
    eq_array=[] #np.zeros((2,20))
#    result_array = np.array([])
    result_array2 = np.zeros(20)
    for filename in os.listdir("../h5/kam"):
        if filename.endswith(".h5"):
            df=pd.read_hdf("../h5/kam/"+filename)
            stats_df=cs.compute_stats(df)
            stats_list=stats_df.values.flatten()[0:20]
#            eq_array=np.append(eq_array,stats_list,axis=1)
#            eq_array.append(stats_list)
#            result_array = np.append(result_array, stats_list)
            result_array2= np.vstack((result_array2, stats_list))
#            i=i+1
#            eq_array=[eq_array;stats_list]
    return result_array2
    
    print("done")

def select_control_plot(df,eq_df): 
    
    
#    dst_y=df2['dst']
    
    df2=df['dst']>-50
    
    df['eq']=np.zeros(dst_df.shape[0])
    
    for index, row in eq_df.iterrows():
        eq_date=datetime.datetime(index.year,index.month,index.day)
        
        D=df.iloc[df.index.get_loc(eq_date,method='nearest')]
        D2=df.index.get_loc(eq_date,method='nearest')
        
#        df.iloc[D.name][2]=1
        for i in range(1,120):
            idx=df.index[D2-i]       
            df=df.set_value([idx],['eq'],1)
        df3=df[(df['dst']>(-50)) & (df['eq'] == 0)]
        df4=df3.between_time('00:00','00:30')
        
        
        
        
        
        
#    print("done")
#    for index, row in df2.iterrows():
#        if df2['dst']:
#            df2['marker']='g'
#        else:
#            df2['marker']='r'
#    
#    start_date=datetime.datetime(2004,2,10)
#    rng=pd.date_range(start_date,freq='1d',periods=1421)
    
    return df4

dst_df=pd.read_hdf("../h5/dst.h5")
eq_df=pd.read_hdf("../h5/eq.h5")


decision_df=select_control_plot(dst_df,eq_df)
#eq_array=load()

dst_mean=stat.mean(dst_df.dst)
dst_std=stat.pstdev(dst_df.dst)

threshold=dst_mean-(2*dst_std)

   
eq_df_candidates=eq_df    
for index, eq in eq_df.iterrows():
    eq_date=datetime.datetime(index.year,index.month,index.day)
    
    if not dst.test_date(dst_df,index,threshold):      
        eq_df_candidates=eq_df_candidates.drop(index)
 
# Need to select most powerful earthquake on given day

       
#for index, eq in eq_df_candidates.iterrows():
#    
#    eq_date=datetime.datetime(index.year,index.month,index.day)
#    vlf.create_hdf5(-1,eq_date)
    
    
    
    
#print("Earthquake at " + str(index) + " is a possible candidate")
    
#    for file in os.listdir("../h5"):
#        df=pd.read_hdf("../h5/"+file,file.split('.')[0])
#        print("done")
        
        
