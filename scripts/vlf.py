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
#Function to condition the vlf data. Ignoring blank data, and 
def condition_vlf():
    print('To be added')

#Function for getting 5 day period before eq/ non-eq
def output(df,date):
    print('To be added')
    
#Old rename function for reference
def old_rename(folder):
    months=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']   
    def month2num(name):
        for month in months:
            if month in name:
                number=months.index(month)+1
                num2=('%02.f' % number)
                newname=name.replace(month,str(num2))
                day=name[1:3]
                #mon=name[3:6]
                newname='t'+str(num2)+'-'+str(day)+'-'+name[6:]
                return(str(newname))
        return name
    
    #Standardise the name for the files
    files=os.listdir()
    for file in files:
        if file.endswith('.kam') or file.endswith('.KAM'):
            newname=file.lower()
            newname2=month2num(newname)
            print('new name: ' + newname2 + ' old name: ' + newname)
            os.rename(file,newname2)
            print(file)
        else:
            files.remove(file)
            print(file+' removed from files string') 