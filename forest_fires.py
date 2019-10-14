# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 21:17:01 2019

@author: black
"""
import pandas as pd
import matplotlib.pyplot as plt
from helper_funcs import to_categorical
import seaborn as sns
fires = pd.read_csv('forest-fires-amazon.csv', encoding = "ISO-8859-1")
fires.set_index('date', drop=True, inplace=True)
#print(pd.unique(fires.year))
fires.drop(columns=['year'], inplace=True)
#print(fires.index.dtype)

fires.index = pd.to_datetime(fires.index)
#print(fires.index.dtype)
#print(pd.unique(fires.month))

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

map_months = dict(zip(pd.unique(fires.month), months))
fires.month = fires.month.map(map_months)

fires = to_categorical(fires, verbose=0)

fires.rename(columns={'number': 'number_of_fires'}, inplace=True)
fires_by_state = fires.groupby(by='state').mean()
fires_by_state.sort_values(by='number_of_fires').plot(kind='bar' , 
                          title='Fires By State (Mean)'); plt.show()

#sns.boxplot(x='number_of_fires', data=fires_by_state)
fires_by_month = fires.groupby(by='month', sort=False).mean()
fires_by_month.sort_values(by='number_of_fires').plot(kind='bar', 
                          title='Fires by Month (Mean)'); plt.show()
fires_by_year = []
lookup = set()
index_unique = [x for x in fires.index.values if x not in lookup and lookup.add(x) is None]

for fire in index_unique:
    fires_by_year.append(fires.loc[fire].mean()[0])

fires_by_year = pd.DataFrame(data=fires_by_year, index=index_unique, 
                             columns=['Fires_per_year'])

fires_by_year.plot(grid=True); plt.title('Average Fires per year in Brazil (Mean)')
plt.xlabel('Year'); plt.ylabel('Fires per annum'); plt.show()
    
fires_by_month_and_state = fires.groupby(by=['month', 'state']).mean().unstack()

#Prepare data to plot 12 most inflicted states history of fire - Too messy? Some code and inspiration from kernel found there
fires = fires.reset_index(); fires.date = fires.date.dt.year
fiery = fires_by_state.sort_values(by='number_of_fires', ascending=False)[:12]
fiery = list(fiery.index.values)
fires.set_index(keys='state', drop=True, inplace=True)
fires_most_by_state = fires.loc[fiery]
fmbsy = fires_most_by_state.groupby(by=['state','date']).mean().reset_index()

#Cannot seem to get the legend right, need to fix? 
plt.figure(figsize=(18,7))
sns.lineplot(x="date", y="number_of_fires", hue="state", data=fmbsy, legend=False)
legend = list(fmbsy.state.unique())
plt.legend(labels=legend) 
plt.xticks(fmbsy["date"])
plt.title("Top 12 states with forest fires over the years")
plt.legend(loc="upper left")
plt.show()

#Plot 15 most inflicted state's mean fire outbursts on each month collectively over the entire series
for month in fires_by_month_and_state.index:
    fires_by_month_and_state.loc[[month]].T.sort_values(by=month, ascending=False).iloc[:15].plot(kind='bar')
    plt.title('Number of fires (Mean) over States on {}'.format(month))
    plt.ylabel('Fires per State'); plt.xlabel('States'); plt.show()
    
