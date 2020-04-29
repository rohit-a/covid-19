# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 12:36:51 2020

@author: rohit

Script to read data from mohfw website and keep statewise and national snapshot of Covid19 cases in India

"""

import requests
import datetime
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.mohfw.gov.in/'
country = 'India'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
state_data_list = []
date = str(datetime.date.today())
cleanup_list = ['#',","]


def clean_value(str_to_clean, cleanup_list=cleanup_list):
    for ch in cleanup_list:
        str_to_clean = str_to_clean.replace(ch,'')
    return str_to_clean

#Extracting Date and overall India data
india_section = soup.find('div', class_='site-stats-count')

#Extracting as of date for data
as_of_date = india_section.find('h2').find('span').text

#Extracting India level counts and adding in list
india_counts = india_section.find('ul').find_all('strong')
ind_c, ind_r, ind_d = india_counts[0].text, india_counts[1].text, india_counts[2].text
state_data_list.append(['0', date, country, 'India', ind_c, ind_r, ind_d, as_of_date])


#Extracting State Section data
state_section = soup.find('section', id='state-data')
state_table = state_section.find('div', class_='data-table table-responsive').find('table')
state_table_rows = state_table.find_all('tr')

#Looping through state table rows. Removing extra rows.
row_processed, row_skipped = 0, 0
for row in state_table_rows:
    cols = row.find_all('td')
    if(len(cols) == 5):    
        s_no = clean_value(cols[0].text)
        state = clean_value(cols[1].text)
        confirmed = clean_value(cols[2].text)
        recovered = clean_value(cols[3].text)
        deaths = clean_value(cols[4].text)
        state_data_list.append([s_no, date, country, state, confirmed, recovered, deaths, as_of_date])
        row_processed = row_processed+1
        print("{} {} Extracting {} data".format(row_processed, s_no, state))
    else:
        row_skipped =row_skipped+1
        print("{} Skipping {}".format(row_skipped, row.text))
print("Extracted {} rows data. Skpped {} rows".format(row_processed, row_skipped))


#Converting to data frame
state_df_update = pd.DataFrame(state_data_list, columns=['S_no','Date', 'Country','State','Confirmed','Recovered','Deaths','As_Of_Date'])
 
#Reading existing file, filtering out duplicate data for today, appending update and writing back.
state_df = pd.read_csv("India Covid19 combined data(mohfw snapshot).csv", header=0, names=['S_no','Date', 'Country','State','Confirmed','Recovered','Deaths','As_Of_Date'])
state_df = state_df[state_df['Date'] != date]
state_df = state_df.append(state_df_update, ignore_index=True)
 
print("Updating CSV for: "+ as_of_date)
state_df.to_csv("India Covid19 combined data(mohfw snapshot).csv")
