#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 11:15:28 2018

@author: isaacmehigan

Flux.py to look at charged particle flux
"""

import os
import pandas as pd
import urllib
import re
import requests
#for filename in os.listdir(""):
#    

def load(file):
    """ Function to load the dst data into a dataframe
    """
#    
    data_start=find_data_start(file,"data:")
    flux_data = pd.read_csv(file,
                       sep=',', 
                       engine='python',
                       index_col='time_tag',
                       skiprows=data_start
                       )

#    flux_data=add_date_col(dst_data)
    return flux_data


def load_all(directory):
    df = pd.DataFrame() #creates a new dataframe that's empty
#    newDF = newDF.append(oldDF, ignore_index = True)
    files=sorted(os.listdir(directory))
    for file in files:
        if file.lower().endswith('.csv') and file.startswith('200'):
            month_df=load(directory+file)
            df=df.append(month_df)
    return df
    
def find_data_start(filepath, keywords):
   with open(filepath) as f:
       for counter, line in enumerate(f, start = 1):
           if line.find(keywords) >= 0:
              return counter   
    

def download(output_dir):
    already_downloaded_files=os.listdir(output_dir)
    counter1=0
    counter2=0
    for year in range(2004,2008):
        for month in range(1,13):
            output_filename=str(year)+"-"+str(month).zfill(2)+"-flux.csv" 
            if output_filename in already_downloaded_files:
#                print(output_filename + " is already downloaded")
                counter1=counter1+1
            else:
                generic='https://satdat.ngdc.noaa.gov/sem/goes/data/avg/YEAR/MON/goes10/csv/'
                directory=generic.replace('YEAR',str(year)).replace('MON',str(month).zfill(2))
                r = requests.get(directory)   
                rt=r.text
                filename=re.search('"(.*eps_1m.*csv)"',rt)[0].replace('"','')
                urllib.request.urlretrieve(directory+filename, output_dir+output_filename)
                counter2=counter2+1
#                print(output_filename + " downloaded")
    print(str(counter2) + " files downloaded " + str(counter1) + " files were already present")


def save(df):
    """ Function to save data""" 
    df.to_hdf('/Users/isaacmehigan/Documents/fyp/h5/flux.h5', 'flux', format = 'table', mode='w')


#flux_data=load("/Users/isaacmehigan/Documents/fyp/flux/data/2004-01-flux.csv")
#file=open("/Users/isaacmehigan/Documents/fyp/flux/data/2004-01-flux.csv")

#flux_df=load_all("/Users/isaacmehigan/Documents/fyp/flux/data/")
save(flux_df[['e1_flux_i','p1_flux']])
#download("/Users/isaacmehigan/Documents/fyp/flux/data/")
#year=2004
#month=1
#generic='https://satdat.ngdc.noaa.gov/sem/goes/data/avg/YEAR/MON/goes10/csv/'
#directory=generic.replace('YEAR',str(year)).replace('MON',str(month).zfill(2))
#print(r.text)

#https://satdat.ngdc.noaa.gov/sem/goes/data/avg/2007/01/goes10/csv/g10_eps_1m_20070101_20070131.csv