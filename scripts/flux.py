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
#    colNames=['DST_name','Version','Base_value','1','2','3','4','5','6','7','8','9','10',
#          '11','12','13','14','15','16','17','18','19','20','21','22','23','24','avg']
    flux_data = pd.read_csv(file,
                       sep=',', 
                       engine='python',
                       index_col=False,
                       header=None,
                       skiprows=215
                       )

#    flux_data=add_date_col(dst_data)
    return flux_data


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
#flux_data=load("/Users/isaacmehigan/Documents/fyp/flux/data/g10_eps_1m_20040101_20040131.csv")
download("/Users/isaacmehigan/Documents/fyp/flux/data/")
#year=2004
#month=1
#generic='https://satdat.ngdc.noaa.gov/sem/goes/data/avg/YEAR/MON/goes10/csv/'
#directory=generic.replace('YEAR',str(year)).replace('MON',str(month).zfill(2))
#print(r.text)

#https://satdat.ngdc.noaa.gov/sem/goes/data/avg/2007/01/goes10/csv/g10_eps_1m_20070101_20070131.csv