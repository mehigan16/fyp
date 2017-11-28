#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 17:56:45 2017
Load and plot the eq data
@author: isaacmehigan
"""

"""
Data structure: 
amplitude phase (NWC transmitter) amplitude phase (NPM) amplitude phase (JJI) amplitude phase (JJY)

JJI is main for EQs
"""
import pandas
import os
import re
import glob
import string
import matplotlib.pyplot as plt
import datetime
import numpy as np
from scipy import stats

##Plot figures in a new window
#from IPython import get_ipython
#get_ipython().run_line_magic('matplotlib', 'qt5')
##

#Functions--------------------------------------------------
def filename2date(filename):
    splits=filename.split('-')
    mon=int(splits[0][1:])
    day=int(splits[1])
    year=2000+int(splits[2][0])
    
    print(mon,day,year)
    
    date=datetime.datetime(year,mon,day)-datetime.timedelta(minutes=1)
    return(date)

def add_date_col(data,file):
    length=len(data.index)
    tmp=data.index
    start_date=filename2date(file)
    rng=pandas.date_range(start_date,freq='20s',periods=length)
    data['time']=rng
    data['num']=tmp
    data2=data.set_index('time')
    return data2

#------------------------------------------------------------

print("Loading the data")

colNames=['A_nwc','P_nwc','A_npm','P_npm','A_jji','P_jji','A_jjy','P_jjy']
#months=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
#Alldata=[0]*8
Alldata=[]
#Alldata = pandas.DataFrame([[], []])
data=[0]*8

files=os.listdir('../kam/eq2/')
os.chdir('../kam/eq2/')
CWD=os.getcwd()

#start_date=files[0]

#for file in files:

for file in files:

    filename=os.path.join(os.getcwd(),file)
    data = pandas.read_csv(filename,
                       sep='\s+', 
                       engine='python',
                       index_col=False,
                       verbose=True,
                       names=colNames,
                       header=None,
                       skiprows=1
                       )
    data=add_date_col(data,file)
#    data['num']=list(range(0,len(Alldata.index)))
    night_data=data.between_time('18:00','8:00')
    Alldata.append(data.iloc[0:1400,:])
    Alldata.append(data.iloc[3700:,:])
Alldata=pandas.concat(Alldata)
All_night_data=Alldata.between_time('18:00','8:00')
#Ajji=min(data.iloc[:,4])
plt.figure(num=None, figsize=(10, 6), dpi=200)

#print(filename)
#np.argmin(data.iloc[:,4])

#N = len(Alldata.index)
##x = np.linspace(0, N, N,endpoint=False)
#x = np.array([datetime.datetime(2004, 1, 9, i, 0) for i in range(24)])
x=All_night_data['num']
y=All_night_data['A_jji']

JJIamp=plt.plot(All_night_data.index[:], All_night_data.iloc[:,4], 'r',All_night_data.index[:],All_night_data.iloc[:,6],'b')

[slope, intercept, r_value, p_value, std_err] = stats.linregress(x,y)

#JJIphase=plt.plot(x, data.iloc[:,5], 'r--')
#JJIamp.show()
#JJIphase.show()

# LATER to append the data
#for file in files:
#    filename=os.path.join(os.getcwd(),file)
#     data = pandas.read_csv(filename,
#                       sep='\s+', 
#                       engine='python',
#                       index_col=False,
#                       header=None,
#                       skiprows=1
#                       )
#    Alldata
#    print(filename)
    


