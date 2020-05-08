"""
Created on Sat Mar 28 18:42:15 2020

@author: rohit
"""

import pandas as pd

##Global files

#reading data from csv files
confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

df_confirmed = pd.read_csv(confirmed_url)
df_recovered = pd.read_csv(recovered_url)
df_deaths = pd.read_csv(deaths_url)

#Coalescing Province/State 
df_confirmed["Province/State"] = df_confirmed["Province/State"].mask(pd.isnull, df_confirmed["Country/Region"]) 
df_deaths["Province/State"] = df_deaths["Province/State"].mask(pd.isnull, df_deaths["Country/Region"])
df_recovered["Province/State"] = df_recovered["Province/State"].mask(pd.isnull, df_recovered["Country/Region"])

#pivoting down data
df_confirmed = df_confirmed.melt(id_vars=["Province/State","Country/Region","Lat","Long"])
df_deaths = df_deaths.melt(id_vars=["Province/State","Country/Region","Lat","Long"])
df_recovered = df_recovered.melt(id_vars=["Province/State","Country/Region","Lat","Long"])

#Renaming,removing columns
df_confirmed = df_confirmed.rename(columns={"variable":"Date","value":"#Confirmed"})
df_deaths = df_deaths.rename(columns={"variable":"Date","value":"#Deaths"})
df_recovered = df_recovered.rename(columns={"variable":"Date","value":"#Recovered"})

df_deaths = df_deaths[["Province/State","Country/Region","Date","#Deaths"]]
df_recovered = df_recovered[["Province/State","Country/Region","Date","#Recovered"]]

#Joining Datasets
df_master = df_confirmed.join(df_deaths.set_index(["Province/State","Country/Region","Date"]), on=["Province/State","Country/Region","Date"], how='outer')
df_master = df_master.join(df_recovered.set_index(["Province/State","Country/Region","Date"]), on=["Province/State","Country/Region","Date"], how='outer')

#output csv
df_master.fillna(0)
df_master.to_csv("covid-19 combined data.csv")

