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
    df[colname] = df[colname].apply(lambda x: 'London' if 'London' in x else x.replace('-', ' '))

def extract_from_dataframe(df, colname):
    df[colname] = df[colname].str.extract(r'(\d{4})')

def convert_to_numbers(df, colname):
    df[colname] = pd.to_numeric(df[colname])

def replace_with_zero(df, colname):
    df[colname] = df[colname].fillna(0)

def replace_columnname(df):
    df.columns = [c.replace(' ', '_') for c in df.columns]

def group_by_country(df):
    return df.groupby(['Country'], as_index=False)

if __name__ == "__main__":
    filename_book = 'Books.csv'
    filename_city = 'City.csv'
    column_name = 'Place of Publication'
    column_name1 = 'Date of Publication'

    df_book = load_csv(filename_book)
    df_city = load_csv(filename_city)

    uniform_the_dataframe(df_book, column_name)

    extract_from_dataframe(df_book, column_name1)

    convert_to_numbers(df_book, column_name1)
    
    replace_with_zero(df_book, column_name1)

    replace_columnname(df_book)

    newdf = pd.merge(df_book, df_city, how='left', left_on='Place_of_Publication', right_on='City')

    after_group = group_by_country(newdf)



