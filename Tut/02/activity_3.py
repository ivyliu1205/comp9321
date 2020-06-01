import pandas as pd
from pymongo import MongoClient

'''
1. Load the CSV file using the method you created in the first activity
2. Install mongodb on your local machine
3. Create a database named comp9321 with a collection named Demographic_Statistics
4. Write the dataframe in mongodb
5. Query the database and load the data into a new dataframe again
'''

def read_csv(filename):
    return pd.read_csv(filename)

def create_mongodb_database(dbname):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    return myclient[dbname]

def create_collection(db, collecname):
    return db[collecname]

if __name__ == "__main__":
    input_filename = 'Demographic_Statistics_By_Zip_Code.csv'
    database_name = 'comp9321'
    collection_name = 'Demographic_Statistics'

    print('== Read the CSV file')
    df = read_csv(input_filename)
    print('!!!Successful!!!\n')
    
    print('== Create a database')
    db = create_mongodb_database(database_name)
    print('!!!Successful!!!\n')

    print('== Create a collection')
    collection = create_collection(db, collection_name)
    print('!!!Successful!!!\n')

########################################
# Unfinished