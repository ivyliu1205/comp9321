import pandas as pd
import re
from flask import Flask
from flask import request
from flask_restplus import fields
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)
df = pd.read_csv('Books.csv')

book_model = api.model('Book', {
    'Flickr_URL': fields.String,
    'Publisher': fields.String,
    'Author': fields.String,
    'Title': fields.String,
    'Date_of_Publication': fields.Integer,
    'Identifier': fields.Integer,
    'Place_of_Publication': fields.String
})

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
    
    def delete(self, id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))
        df.drop(id, inplace=True)
        return {"message": "Book {} is removed.".format(id)}, 200
    
    @api.expect(book_model)
    def put(self, id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))
        book = request.json
        if 'Identifier' in book and id != book['Identifier']:
            return {"message": "Identifier cannot be changed"}, 400
        
        for key in book:
            if key not in book_model.keys():
                return {"message": "Property {} is invalid".format(id)}, 400
            
        return {"message", "Book {} has been successfully updated",format(id)}, 200

if __name__ == "__main__":
    clean_data(df)
    app.run(host='127.0.0.1',port=8000, debug=True)


