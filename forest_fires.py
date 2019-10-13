# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 21:17:01 2019

@author: black
"""
import pandas as pd
import matplotlib.pyplot as plt
fires = pd.read_csv('forest-fires-amazon.csv', encoding = "ISO-8859-1")
fires.set_index('year', drop=True, inplace=True)
print(pd.unique(fires.date))
fires.drop(columns=['date'], inplace=True)
print(fires.index.dtype)
fires.index = pd.to_datetime(fires.index)
print(fires.index.dtype)
print(pd.unique(fires.month))

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

map_months = dict(zip(pd.unique(fires.month), months))
fires.month = fires.month.map(map_months)