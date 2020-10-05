#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 05:35:53 2020

@author: ece-student
"""

# Import COVID-19 Data API
import COVID19Py
import matplotlib.pyplot as plt
import pandas as pd

# Access the COVID19Py API
covid = COVID19Py.COVID19(url="https://cvtapi.nl")

# Process Data
location = covid.getLocationByCountryCode("US", timelines=True)
raw_data = location[0]['timelines']['confirmed']['timeline']
covid_data = pd.DataFrame.from_dict(raw_data, orient = 'index')
covid_data = covid_data.reset_index()
covid_data.columns = ['Date','Confirmed Cases']
covid_data['Date'] = pd.to_datetime(covid_data.Date, format='%Y-%m-%dT%H:%M:%SZ')
print(covid_data)

# Plot Data
fig = plt.plot(covid_data['Date'], covid_data['Confirmed Cases'])
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Confimed Cases of COVID-19')
plt.title('Cases of COVID-19 in the United States')
plt.show()
