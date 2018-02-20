#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:30:38 2018

@author: isaacmehigan

Pre-modelling

"""


import dst as dst
#import vlf as vlf
#import eq as eq
#import compute_stats as cs
import os
import pandas as pd
import datetime


def load():
    print("done")
    
def test_date(df,date,*threshold):
    """ Function to check if the dst value was below the threshold on the
    5 days leading to the given datetime. threshold is -50 if nothing given.
    """
    
    D=df.iloc[df.index.get_loc(date,method='nearest')]
    date=D.name
    lower_date=date-datetime.timedelta(days=5)
    upper_date=date +datetime.timedelta(hours=1)
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
#        print("Warning at least 1 value in the time range was below threshold")
        return 1
    else:
        return 0





dst_df=pd.read_hdf("../h5/dst.h5")
eq_df=pd.read_hdf("../h5/eq.h5")
    
eq_candidates=[]    
for index, eq in eq_df.iterrows():
    index.date    
    if test_date(dst_df,index):
        print("Earthquake at " + str(index) + " is a possible candidate")
        eq_candidates.append(eq)
    
    
#    for file in os.listdir("../h5"):
#        df=pd.read_hdf("../h5/"+file,file.split('.')[0])
#        print("done")
        
        
#load()