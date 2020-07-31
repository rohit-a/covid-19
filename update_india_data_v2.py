# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 18:42:51 2020

@author: rohit
"""
import requests
import datetime
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.mohfw.gov.in/'
URL_json = 'https://www.mohfw.gov.in/data/datanew.json'
country = 'India'

date = str(datetime.date.today())
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

#Extracting as of date from website
india_section = soup.find('section', id='site-dashboard').find('div',class_='status-update')
as_of_date = india_section.find('span').text
as_of_date = as_of_date.splitlines()[0]

state_df_update = pd.read_json(URL_json)
state_df_update['Country'] = country
state_df_update['Date'] = date
state_df_update['As_Of_Date'] = as_of_date

state_df_update['state_name'].replace('','Total',inplace=True)
state_df_update['state_name'].replace('Telengana***','Telengana',inplace=True)
state_df_update['state_name'].replace('Telengana','Telangana',inplace=True)

state_df_update.rename({'sno':'S_no', 'state_name':'State','new_positive':'Confirmed','new_cured':'Recovered','new_death':'Deaths'}, inplace=True, axis=1)

#Check mismatch
total_mismatch = state_df_update['Confirmed'] != (state_df_update['new_active'] + state_df_update['Recovered'] + state_df_update['Deaths'])
print("Mismatch States:"+str(state_df_update[total_mismatch]['State'].values))
state_df_update.loc[total_mismatch,'Confirmed'] = state_df_update['new_active'] + state_df_update['Recovered'] + state_df_update['Deaths']

#Reading existing file, filtering out duplicate data for today, appending update and writing back.
state_df = pd.read_csv("India Covid19 combined data(mohfw snapshot).csv", header=0, names=['S_no','Date', 'Country','State','Confirmed','Recovered','Deaths','As_Of_Date'])
state_df = state_df[state_df['Date'] != date]
state_df = state_df.append(state_df_update[['S_no', 'Date', 'Country', 'State', 'Confirmed', 'Recovered', 'Deaths', 'As_Of_Date' ]], ignore_index=True)
 
print("Updating CSV for: "+ as_of_date)
state_df.to_csv("India Covid19 combined data(mohfw snapshot).csv")