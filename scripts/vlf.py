#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:21:07 2017

@author: isaacmehigan
"""

#Kam load

import os
import re
import datetime
from time import strptime
import pandas as pd


def rename(folder):
    """ Function to rename the files to a useful timestamp filename
    The old naming convention: T23FEB4A.kam
    New naming convention: 2004-02-23.kam
    """
    files=os.listdir(folder)
#    files=['T23FEB04A.kam','t06mar04a.kam']
    os.chdir(folder)
    for file in files:
#        string='T23FEB04A.kam'
        if file.lower().endswith('.kam') and not file.startswith('2'):
            search=r'(\d\d)([a-zA-Z]{3})(\d)'
            match=re.split(search,file)
            new_format='%Y-%m-%d.kam'
            year=2000+int(match[3])
            mon=int(strptime(match[2],'%b').tm_mon)
            day=int(match[1])
            file_date=datetime.datetime(year,mon,day)
            new_name=file_date.strftime(new_format)
            print(file," goes to: ",new_name)
            os.rename(file,new_name)
        elif file.lower().endswith('.kam') and file.startswith('2'):
            break
        else:
            print(file, " is not a .kam file")
        

#Function to load the year of data being used and return a pandas dataframe of the data
def load(year):
    print('To be added')
#    files=os.listdir('../kam/'+year)
#    os.chdir('../kam/'+year)    
#    return df
    
def condition(file):
    """ Fuction to condition the data by adding collumn names and index timestamp
    Need to add searching for zero data in the future.
    """
    colNames=['A_nwc','P_nwc','A_npm','P_npm','A_jji','P_jji','A_jjy','P_jjy']
    file_name=os.path.join(os.getcwd(),file)
    file_date=datetime.datetime.strptime(file,'%Y-%m-%d.kam')
    data = pd.read_csv(file_name,
                       sep='\s+', 
                       engine='python',
                       index_col=False,
                       verbose=True,
                       names=colNames,
                       header=None,
                       skiprows=1
                       )
    data=add_date_col(data,file_date)
    return data
    
def add_date_col(data,start_date):
    """ Function to add the timestamp for the file as the index col
    """
    length=len(data.index)
    tmp=data.index
    start_date=start_date-datetime.timedelta(minutes=1)
    rng=pd.date_range(start_date,freq='20s',periods=length)
    data['time']=rng
    data['num']=tmp
    data2=data.set_index('time')
    return data2

def create_hdf5(date1,date2):
    """ Function to make a hdf5 for .kam data between 2 dates
    Also works if only 1 date is entered, this gives data 5 days before an EQ 
    """
    new_format='%Y-%m-%d.kam'
    folder="/Users/isaacmehigan/Documents/fyp/kam/data"
    if (type(date1) is datetime.datetime):
        print("2 arguments generating hdf5 for ",date1.strftime('%Y-%m-%d')," to ",date2.strftime('%Y-%m-%d'))
        output_filename=(datetime.datetime.strftime(date2,'../output/%Y-%m-%d') +
        datetime.datetime.strftime(date2,'_%Y-%m-%d.h5'))
    else:
        print("1 argument ",date2.strftime('%Y-%m-%d')," so generating data for 5 days before")
        date1=date2 - datetime.timedelta(days=5)
        output_filename=datetime.datetime.strftime(date2,'../output/eq_%Y-%m-%d.h5')
    
    date_0=datetime.datetime(2004,2,14) #set lowest date allowed
    date_n=datetime.datetime(2007,12,31) #set highest date allowed
    
    if not ((date_0 < date1 < date_n) or (date_0 < date2 < date_n)):
        print("Dates are outside of data range")
    else:
        print("Dates are within data range")
    output_df=[]
    os.chdir(folder)
#        files=os.listdir(folder)
    numdays=(date2-date1).days + 2 #To include the first 3 samples for date2
    date_list = [date1 + datetime.timedelta(days=x) for x in range(0, numdays)]
    for date in date_list:
        file=datetime.datetime.strftime(date,new_format)
        df=condition(file)
        output_df.append(df)
    output_df=pd.concat(output_df)
    num=len(output_df.index)
    output_df['num']=range(0,num)
    output_night_df=output_df[date1:date2].between_time('18:00','8:00')
    output_night_df.to_hdf(output_filename,'eq_df',format='table')
    print("File",output_filename.split("/")[-1],"was created")