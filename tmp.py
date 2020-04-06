# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:08:41 2020

@author: rohit
"""

import pandas as pd
pivot_key_columns = ["UID","iso2","iso3","code3","FIPS","Admin2","Province_State","Country_Region","Lat","Long_","Combined_Key"]
group_key_columns = pivot_key_columns.copy()
group_key_columns.append("Date")

#Reading csv files
df_us_confirmed = pd.read_csv("C:/Users/rohit/Documents/GitHub/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
df_us_deaths = pd.read_csv("C:/Users/rohit/Documents/GitHub/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv")

df_us_confirmed = df_us_confirmed.fillna(0)
df_us_deaths = df_us_deaths.fillna(0)

#pivoting down data
df_us_confirmed = df_us_confirmed.melt(id_vars=pivot_key_columns, var_name="Date", value_name="#Confirmed" )
df_us_deaths = df_us_deaths.melt(id_vars=pivot_key_columns, var_name="Date", value_name="#Deaths")


#QA Reference Value
sumConfPre = sum(df_us_confirmed["#Confirmed"])
sumDeathPre = sum(df_us_deaths["#Deaths"]) 

#Append data frames
df_us_combined = df_us_confirmed.append(df_us_deaths)
df_us_combined = df_us_combined.groupby(group_key_columns).sum()

#Final Values after pivot
sumConfPost = sum(df_us_combined["#Confirmed"])
sumConfPre = sum(df_us_combined["#Deaths"])

if sumConfPre == sumConfPost and sumDeathPre ==sumDeathPost:
    

