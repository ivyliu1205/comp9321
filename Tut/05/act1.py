import pandas as pd
import re
from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)
df = pd.read_csv('Books.csv')

def clean_data(df):
    columns_to_drop = ['Edition Statement',
                        'Corporate Author',
                        'Corporate Contributors',
                        'Former owner',
                        'Engraver',
                        'Contributors',
                        'Issuance type',
                        'Shelfmarks']
    df.drop(columns_to_drop, inplace=True, axis=1)
    df['Place of Publication'] = df['Place of Publication'].apply(lambda x: clean_pop(x))
    df['Date of Publication'] = df['Date of Publication'].str.extract(r'(\d{4})', expand=False).fillna(0)
    pd.to_numeric(df['Date of Publication'])
    df.set_index('Identifier', inplace=True)
    df.columns = df.columns.str.replace(' ', '_')
    #print(df.to_string())

def clean_pop(str):
    if (str.find('London') != -1):
        return 'London'
    elif (str.find('_') != -1):
        return re.sub('_', ' ', str)
    else:
        return str

@api.route('/<int:id>')
class Books(Resource):
    def get(self, id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))
        book = dict(df.loc[id])
        return book

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == "__main__":
    clean_data(df)
    app.run(debug=True)


