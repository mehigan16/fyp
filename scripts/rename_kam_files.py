#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 18:00:20 2017
Rename the kam files to have them in a suitable order
@author: isaacmehigan
"""

import pandas
import os
import re
import glob
import string
print("Loading the data")
months=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']

bigArray=[]

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

 
print('---------------------------')

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
        