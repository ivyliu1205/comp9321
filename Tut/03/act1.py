import pandas as pd

def read_csv(filename):
    return pd.read_csv(filename)

def print_dataframe(df):
    print(','.join(str(col) for col in df))
    
    for index, rows in df.iterrows():
        print(','.join(str(rows[col]) for col in df))

def print_nan(df):
    print('\n')
    print(df.isna().sum())

def drop_columns(df, columns_to_drop):
    print('\nBefore drop:\n' + ','.join(str(col) for col in df))
    df.drop(columns_to_drop, inplace=True, axis=1)
    print('\nAfter drop:\n' + ','.join(str(col) for col in df))

if __name__ == "__main__":
    filename = 'Books.csv'
    columns_to_drop = [
        'Edition Statement',
        'Corporate Author',
        'Corporate Contributors',
        'Former owner',
        'Engraver',
        'Contributors',
        'Issuance type',
        'Shelfmarks'
    ]

    df = read_csv(filename)
    print_dataframe(df)

    print_nan(df)

    drop_columns(df, columns_to_drop)
