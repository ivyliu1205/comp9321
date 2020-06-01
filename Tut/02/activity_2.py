import pandas as pd
from pandas.io import sql

import sqlite3
import sys

'''
1. Load the CSV file using the method you created in the previous activity
2. Store the dataframe in sqlite database
3. Query the database and load the data into a new dataframe again
'''

def read_csv(filename):
    return pd.read_csv(filename)

def store_in_sqlite(dataframe, tablename, dbname):
    conn = sqlite3.connect(dbname)

    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS ' + tablename)

    sql.to_sql(dataframe, name=tablename, con=conn)

def make_queries(dbname, tablename):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    while(1):
        try:
            query = input('Enter your query: ')
            # load the answer into a new dataframe 'newdf'
            newdf = pd.read_sql_query(query, conn)
            # print the answer
            print(','.join(str(col) for col in newdf))
            for index, row in newdf.iterrows():
                print(','.join(str(row[col]) for col in newdf))
        except KeyboardInterrupt:
            print('\nExit query time\n')
            break
    cursor.close()
    conn.commit()

if __name__ == '__main__':
    input_filename = 'Demographic_Statistics_By_Zip_Code.csv'
    table_name = 'Demographic_Statistic'
    database_name = 'Demographic.db'

    dataframe = read_csv(input_filename)
    print('Load the CSV file successfully\n')

    store_in_sqlite(dataframe, table_name, database_name)
    print('Store the dataframe in sqlite database successfully\n')
    
    print('Enter query time (Press Ctrl-C to exit :) )')
    make_queries(database_name, table_name)
