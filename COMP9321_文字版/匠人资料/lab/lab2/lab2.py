#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 13:43:13 2019

@author: alexlo
"""

import pandas as pd
#pd.set()
file = 'Books.csv'
df = pd.read_csv(file)
#print(df.isna().sum())
#to show the number of null value in each column

num_of_rows = df.shape[0]
columns_to_drop=[]
for column in df:
    # df[column].isnull() : returns an array of True/False showing the cell is null or not
    percent = 100 * df[column].isnull().sum() / num_of_rows
#    print(column, str(percent) + '%')
    if percent > 0:
        columns_to_drop.append(column)
#print(columns_to_drop)

def replace(x):
    if 'London' in x:
        return 'London'
    elif ' ' in x:
        return x.replace(' ','_')
    else:
        return x

#print(df['Place of Publication'])
#df['Place of Publication'] = df['Place of Publication'].apply(
#        lambda x: 'London' if 'London' in x else x.replace('-', ' '))

df['Place of Publication'] = df['Place of Publication'].apply(replace)
#print(df['Date of Publication'])
df['Date of Publication'] = df['Date of Publication'].fillna(0)
#print(df['Date of Publication'])
new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
#df['Date of Publication'] = df['Date of Publication'].str.extract(r'^(/d{4})',expand=False)
df['Date of Publication'] = new_date.fillna(0)
#print(df['Date of Publication'])

place = df['Place of Publication']
#print(place)
chart = place.value_counts().plot.bar()

#chart = place.value_counts().plot.pie()

iris = pd.read_csv('iris.csv')
#print(iris)
species = iris['species']
#print(species.value_counts())

versicolor = iris.query("species == 'versicolor'")
#print(versicolor)

virginica = iris[iris['species']=='virginica']
#print(virginica)

setosa = iris[iris['species']=='setosa']
#print(setosa)

versicolor.plot.kde()
#kernal estimation
pd.scatter_matrix(virginica)

import matplotlib.pyplot as plt
fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(10,5))

a1 = versicolor.plot(kind = 'scatter', x='sepal_length', y='sepal_width',c='green',label='versicolor', ax=axes[0])
a2 = virginica.plot(kind = 'scatter', x='sepal_length', y='sepal_width',c='black',label='virginica',ax=a1)
a3 = setosa.plot(kind = 'scatter', x='sepal_length', y='sepal_width',c='red',label='setosa',ax=a1)

b1 = versicolor.plot(kind = 'scatter', x='petal_length', y='petal_width',c='green',label='versicolor', ax=axes[1])
b2 = virginica.plot(kind = 'scatter', x='petal_length', y='petal_width',c='black',label='virginica',ax=b1)
b3 = setosa.plot(kind = 'scatter', x='petal_length', y='petal_width',c='red',label='setosa',ax=b1)
plt.show()