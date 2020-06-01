import pandas as pd

'''
1. Download the dataset
2. Read the CSV file and put the samples into a pandas' dataframe.
3. Programmatically print the columns of the dataframe
4. Programmatically print the rows of the dataframe
5. Save the dataframe as a CSV file
'''

def read_csv(filename):
    return pd.read_csv(filename)

def write_into_csv(dfname, filename):
    dfname.to_csv(filename)

def print_column(dfname):
    for col in dfname:
        print(col)

def print_row(dfname):
    for index, row in dfname.iterrows():
        print(','.join(str(row[col]) for col in df))

if __name__ == '__main__':
    input_filename = 'Demographic_Statistics_By_Zip_Code.csv'
    output_filename = 'finished_one.csv'

    print('== Read the CSV file')
    df = read_csv(input_filename)
    print('!!!Successful!!!\n')
    
    print('== Print columns')
    print_column(df)
    print('!!!Successful!!!')

    print('== Print rows')
    print_row(df)
    print('!!!Successful!!!')

    print('== Write into CSV file')
    write_into_csv(df, output_filename)
    print('!!!Successful!!!')




