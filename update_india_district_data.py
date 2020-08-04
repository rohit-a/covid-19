# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 18:22:11 2020

@author: rohit
"""
import urllib.request, json, pandas as pd

URL = "https://api.covid19india.org/v4/data-all.json"
counts = ['confirmed','deceased','recovered','tested']
state_map = {'AN':'Andaman and Nicobar Islands','AP':'Andhra Pradesh','AR':'Arunachal Pradesh','AS':'Assam','BR':'Bihar','CH':'Chandigarh',
             'CT':'Chhattisgarh','DN':'Dadra and Nagar Haveli and Daman and Diu','DL':'Delhi','GA':'Goa','GJ':'Gujarat','HR':'Haryana',
             'HP':'Himachal Pradesh','JK':'Jammu and Kashmir','JH':'Jharkhand','KA':'Karnataka','KL':'Kerala','LA':'Ladakh', 'LD':'Lakshadweep',
             'MP':'Madhya Pradesh','MH':'Maharashtra','MN':'Manipur','ML':'Meghalaya','MZ':'Mizoram', 'NL':'Nagaland','OR':'Odisha',
             'PY':'Puducherry','PB':'Punjab','RJ':'Rajasthan','SK':'Sikkim','TN':'Tamil Nadu','TG':'Telangana', 'TR':'Tripura',
             'UP':'Uttar Pradesh','UT':'Uttarakhand','WB':'West Bengal','TT':'Total','UN':'Unknown'}



def get_counts(data_dict, keys=counts):
    """ returns coalesced 'keys' values from 'data_dict' """
    return (data_dict.get(k,0) for k in keys)


def get_all_data():
    """ returns data frame with data for all states, districts and dates """
    with urllib.request.urlopen(URL) as url:
        data = json.loads(url.read().decode())
    data_arr = []
    for date, date_data in data.items():
        for state, state_data in date_data.items():
            state_name = state_map[state]
            if 'total' in state_data.keys():
                total, deaths, recovered, tested = get_counts(state_data['total'])
                record = (date, state_name, 'Total', total, recovered, deaths, tested)
                data_arr.append(record)
                
            if 'districts' not in state_data.keys():
                continue
            
            for district, district_data in state_data['districts'].items():
                if 'total' in district_data.keys():
                    total, deaths, recovered, tested = get_counts(district_data['total'])
                    record = (date, state_name, district, total, recovered, deaths, tested)
                    data_arr.append(record)
            
    df = pd.DataFrame(data_arr, columns=('Date','State','District','Confirmed','Recovered','Deaths','Tested'))
    df['Date'] = pd.to_datetime(df['Date'])
    return df
       
data_df = get_all_data()
data_df.to_csv("India Covid-19 District Data(covid19 india org).csv")