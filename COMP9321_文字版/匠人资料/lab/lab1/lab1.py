#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:14:30 2019
9321 lab1
@author: alexlo
"""
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

conn = sqlite3.connect('db.db')
file_name = 'Demographic_Statistics_By_Zip_Code.csv'
df = pd.read_csv(file_name)
#print(','.join([column for column in df]))
#for index, row in df.iterrows():
#    print(",".join([str(row[column]) for column in df]))
df.to_sql('table1',conn,if_exists='replace')
cu = conn.execute("select * from table1")
print(cu.description)
conn.close()