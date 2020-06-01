import pandas as pd

def load_csv(filename):
    return pd.read_csv(filename)

def print_dataframe(df, col, row):
    if (col):
        print(','.join(str(col) for col in df))
    if (row):
        for index, row in df.iterrows():
            print(','.join(str(row[col]) for col in df))

def uniform_the_dataframe(df, colname):
    print('\nBefore uniform:\n')
    for index, row in df.iterrows():
        print(str(row[colname]))
    
    df[colname] = df[colname].apply(lambda x: 'London' if 'London' in x else x.replace('-', ' '))

    print('\nAfter uniform:\n')
    for index, row in df.iterrows():
        print(str(row[colname]))

def extract_from_dataframe(df, colname):
    print('\nBefore uniform:\n')
    for index, row in df.iterrows():
        print(str(row[colname]))
    
    df[colname] = df[colname].str.extract(r'(\d{4})')
    
    print('\nAfter uniform:\n')
    for index, row in df.iterrows():
        print(str(row[colname]))

def convert_to_numbers(df, colname):
    df[colname] = pd.to_numeric(df[colname])

def replace_with_zero(df, colname):
    print('\nBefore replace:\n')
    for index, row in df.iterrows():
        print(str(row[colname]))
    
    df[colname] = df[colname].fillna(0)

    print('\nAfter replace:\n')
    for index, row in df.iterrows():
        print(str(row[colname]))

if __name__ == "__main__":
    filename = 'Books.csv'
    column_name = 'Place of Publication'
    column_name1 = 'Date of Publication'

    df = load_csv(filename)

    uniform_the_dataframe(df, column_name)

    extract_from_dataframe(df, column_name1)

    convert_to_numbers(df, column_name1)
    
    replace_with_zero(df, column_name1)



