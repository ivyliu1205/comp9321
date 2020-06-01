# Yiting Liu z5211008
# COMP9321 Assignment2_Data Service for World Bank Economic Indicators
# Python 3.7.3
# Sqlite3
import sqlite3
from sqlite3 import Error

import requests
import json
import ast
import operator

from datetime import datetime
from pandas.io.json import json_normalize

from flask import Flask
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse

# Initialization
app = Flask(__name__)
api = Api(app,
        default='Indicators',
        title='Indicator Collection',
        description='This is a data service for world bank economic indicators')

db = 'z5211008.db'
locationDict = {}
LOCATIONINDEX = 1

# Define parsers
parser_one = reqparse.RequestParser()
parser_one.add_argument('indicator_id', required=True)

parser_two = reqparse.RequestParser()
parser_two.add_argument('order_by')

parser_three = reqparse.RequestParser()
parser_three.add_argument('query')

# create a database connection to the sqlite database
def create_connection(dbname):
    conn = None
    try:
        conn = sqlite3.connect(dbname)
        return conn
    except Error as e:
        print(e)

    return conn

# create a table with sql statement
def create_table(conn):
    create_table = """ CREATE TABLE IF NOT EXISTS Worldbanks (
                            id                  integer PRIMARY KEY,
                            indicator_id        text,
                            indicator_value     text,
                            country_date_value  text,
                            creation_time       text
                        );"""
    c = conn.cursor()
    try:
        c.execute(create_table)
    except Error:
        print('The TABLE Worldbanks already exists')
    conn.commit()

# Insert json into TABLE Worldbanks in sqlite
def insert_data(conn, json_data, indicator_id):
    c = conn.cursor()

    # Find the id of the given data
    global LOCATIONINDEX
    if (id not in locationDict):
        locationDict[indicator_id] = LOCATIONINDEX
        LOCATIONINDEX += 1
    data_id = locationDict[indicator_id]

    # Extract 'country' column to a string
    otherList = []
    for data in json_data:
        indicator_value = data['indicator']['value']
        if (data['value'] != None):
            tuple = (data['country']['value'], data['date'], data['value'])
            otherList.append(tuple)
    others = '),('.join(str(item) for item in otherList)

    currentTime = str(datetime.now().isoformat() + 'Z')
    
    c.execute("INSERT INTO Worldbanks VALUES (?,?,?,?,?)", (data_id, indicator_id, indicator_value, others, currentTime))

    conn.commit()
    c.close()

# Initialize the locationDict after restart
def initialize_locationDict(conn):
    c = conn.cursor()
    c.execute('SELECT id, indicator_id FROM Worldbanks')
    if (len(c.fetchall()) > 0):
        for record in c.fetchall():
            if (record[1] not in locationDict):
                locationDict[1] = record[0]
                LOCATIONINDEX = max(locationDict.values()) + 1

# Retrive the order in orderString, and return a string can be used by sqlite
def insert_into_orderdict(orderString):
    orderDict = {}
    orderLocDict = {}
    orderList = orderString.split(',')
    i = 0
    for col in orderList:
        if (col.find('-') == -1 and col.find('+') == -1):
            ascend = 'ASC'
            colname = col
        else:
            if col[0] == '-':
                ascend = 'DESC'
            else:
                ascend = 'ASC'
            colname = col[1:]

        if (colname not in orderLocDict):
            orderLocDict[colname] = i
            orderDict[i] = ascend
            i += 1

    j = 0
    resultList = []
    for j in range(len(orderLocDict)):
        keyList = list(orderLocDict.keys())
        valList = list(orderLocDict.values())
        col = keyList[valList.index(j)]
        tmpStr = col + ' ' + orderDict[j]
        resultList.append(tmpStr)
    return ','.join(r for r in resultList)

@api.route('/collections')
class Indicators(Resource):
    @api.response(201, 'Collection Created Successfully')
    @api.response(400, 'Validation Error')
    @api.response(404, 'Not found valid data')
    @api.expect(parser_one, validation=False)
    @api.doc(description='Question 1')
    def post(self):
        
        args = parser_one.parse_args()
        id = args.get('indicator_id').strip()
        
        # Download json from a certain url
        source_url = 'http://api.worldbank.org/v2/countries/all/indicators/{}?date=2012:2017&format=json&per_page=1000'.format(id)
        raw_data = requests.get(source_url).json()
        # If the url in invalid(indicator id is invalid)
        if len(raw_data) < 2:
            return {"message": "Please enter a valid indicator ID"}, 404
        
        source_data = raw_data[1]
        conn = create_connection(db)
        if conn is None:
            return {"message": "Connot connect with the database"}, 400
        
        c = conn.cursor()
        try:
            c.execute("SELECT * From Worldbanks WHERE indicator_id=?", (id,))
            if (len(c.fetchall()) == 0):
                insert_data(conn, source_data, id)
        except Error:
            create_table(conn)
            insert_data(conn, source_data, id)
        
        c.execute("SELECT creation_time FROM Worldbanks WHERE indicator_id=?", (id,))
        creation_time = c.fetchall()[0][0]
        conn.close()

        return {
            "uri": "/collections/{}".format(locationDict[id]),
            "id": locationDict[id],
            "creation_time": creation_time,
            "indicator_id": id
        }, 201

    @api.response(200, 'Collections are showed successfully')
    @api.response(400, 'Validation Error')
    @api.response(404, 'Not found valid collection')
    @api.expect(parser_two, validation=False)
    @api.doc(description='Question 3')
    def get(self):
        args = parser_two.parse_args()
        order = args.get('order_by')
        
        # Connect with the database
        conn = create_connection(db)
        if conn is None:
            return {"message": "Connot create the database connection"}, 400
        
        c = conn.cursor()
        # if no order
        if (order == None):
            try:
                c.execute('SELECT * FROM Worldbanks')
                records = c.fetchall()
                if (len(records) == 0):
                    return {"message": "No collections in database"}, 404
                else:
                    result = []
                    for record in records:
                        each = {
                            "uri": "/collections/{}".format(record[0]),
                            "id": record[0],
                            "creation_time": record[4],
                            "indicator_id": record[1]
                        }
                        result.append(each)
                    return result, 200
            except Error:
                return {"message": "No collections in database"}, 404
        
        else:
            order = order.replace(' ', '')
            orderStr = insert_into_orderdict(order)
            try:
                c.execute('SELECT * FROM Worldbanks ORDER BY ' + orderStr)
                records = c.fetchall()
                if (len(records) == 0):
                    return {"message": "No collections in database"}, 404
                else:
                    result = []
                    for record in records:
                        each = {
                            "uri": "/collections/{}".format(record[0]),
                            "id": record[0],
                            "creation_time": record[4],
                            "indicator_id": record[1]
                        }
                        result.append(each)
                    return result, 200
            except Error:
                return {"message": "No collections in database"}, 404

@api.route('/collections/<int:id>')
class IndicatorWithID(Resource):
    @api.response(200, 'Collection Deleted Successfully')
    @api.response(400, 'Validation Error')
    @api.response(404, 'Not found valid data')
    @api.doc(description='Question 2')
    def delete(self, id):
        # Connect with the database
        conn = create_connection(db)
        if conn is None:
            return {"message": "Connot create the database connection"}, 400
        c = conn.cursor()
        
        # Find the collection with location_id = id
        try:
            c.execute('SELECT * FROM Worldbanks WHERE id=?', (id,))
            record = c.fetchall()
            if (len(record) == 0):
                return {"message": "ID doesn't exists"}, 404
        except Error:
            return {"message": "ID doesn't exists"}, 404
        
        # DELETE the collection
        c.execute('DELETE FROM Worldbanks WHERE id=?', (id,))
        conn.commit()
        # Check the collection has been deleted successfully or not
        c.execute('SELECT * FROM Worldbanks WHERE id=?', (id,))
        record = c.fetchall()
        if (len(record) != 0):
            return {"message": "Fail to delete the collection"}, 400
        
        # Remove location id from locationDict
        for key, values in locationDict.items():
            if (values == 1):
                del locationDict[key]
                break

        return {
            "message": "The collection {} was removed from the database!".format(id),
            "id": id
        }, 200

    @api.response(200, 'Collections are showed successfully')
    @api.response(400, 'Validation Error')
    @api.response(404, 'Not found valid collection')
    @api.doc(description='Question 4')
    def get(self, id):
        # Connect with the database
        conn = create_connection(db)
        if conn is None:
            return {"message": "Connot create the database connection"}, 400
        c = conn.cursor()
        if (id not in locationDict.values()):
            return {"message": "Invalid ID"}, 404
        
        try:
            c.execute('SELECT * FROM Worldbanks WHERE id = ?', (id,))
            record = c.fetchall()
            if (len(record) == 0):
                return {"message": "No collection"}, 404
            else:
                entryList = []
                for i in record[0][3].split('),('):
                    tuple = eval(i)
                    resStr = '{"country": ' + tuple[0] + '"date": ' + str(tuple[2]) + '"value": ' + str(tuple[1]) + '}'
                    entryList.append(resStr)

                return{
                    "id": id,
                    "indicator": record[0][1],
                    "indicator_value": record[0][2],
                    "creation_time": record[0][4],
                    "entries": [ele for ele in entryList]
                }, 200

        except Error:
            return {"message": "Invalid ID"}, 404

@api.route('/collections/<int:id>/<int:year>/<string:country>')
class IndicatorWithDetail(Resource):
    @api.response(200, 'Collection is showed successfully')
    @api.response(400, 'Validation Error')
    @api.response(404, 'Not found valid collection')
    @api.doc(description='Question 5')
    def get(self, id, year, country):
        # Connect with the database
        conn = create_connection(db)
        if conn is None:
            return {"message": "Connot create the database connection"}, 400
        c = conn.cursor()
        if (id not in locationDict.values()):
            return {"message": "Invalid ID"}, 404
        country = country.strip()
        try:
            c.execute('SELECT * FROM Worldbanks WHERE id = ?',(id,))
            record = c.fetchall()
            if (len(record) == 0):
                return {"message": "No collection"}, 404
            else:
                find = False
                for i in record[0][3].split('),('):
                    tuple = eval(i)
                    if (tuple[0] == country and tuple[1] == str(year)):
                        value = tuple[2]
                        find = True
                        break
                
                if (find):
                    return {
                        "id": id,
                        "indicator": record[0][1],
                        "country": country,
                        "year": year,
                        "value": float(value)
                    }, 200
                else:
                    return {"message": "Invalid year and/or country"}, 404

        except Error:
            return {"message": "Invalid ID"}, 404

@api.route('/collections/<int:id>/<int:year>')
@api.expect(parser_three, validation=False)
class IndicatorWithQuery(Resource):
    @api.response(200, 'Collections are showed successfully')
    @api.response(400, 'Validation Error')
    @api.response(404, 'Not found valid collection')
    @api.doc(description='Question 6')
    def get(self, id, year):
        args = parser_three.parse_args()
        query = args.get('query')
        
        # Connect with the database
        conn = create_connection(db)
        if conn is None:
            return {"message": "Connot create the database connection"}, 400
        c = conn.cursor()
        if (id not in locationDict.values()):
            return {"message": "Invalid ID"}, 404

        # Extract query
        if (query == None):
            nCountry = -1
        else:
            query = query.strip().replace(' ', '')
            ascending = True
            # N
            if (query.find('-') == -1 and query.find('+') == -1):
                try:
                    nCountry = int(query)
                except ValueError:
                    return {"message": "Invalid query"}, 400
            else:
                if (query.find('-') != -1):
                    ascending = False

                try:
                    nCountry = int(query[1:])
                except ValueError:
                    return {"message": "Invalid query"}, 400
        
        try:
            c.execute('SELECT * FROM Worldbanks WHERE id = ?',(id,))
            record = c.fetchall()
            if (len(record) == 0):
                return {"message": "No collection"}, 404
            else:
                find = False
                entryList = []
                tpleList = record[0][3].split('),(')
                tupleList = []
                for ele in tpleList:
                    tupleList.append(eval(ele))

                tupleList.sort(key = operator.itemgetter(2), reverse=True)
                for tuple in tupleList:
                    if (tuple[1] == str(year)):
                        country = tuple[0]
                        value = tuple[2]
                        string = '{"country": ' + country + ', "value": ' + str(value) + '}'
                        entryList.append(string)
                        find = True

                if (find):
                    # No query
                    if (nCountry == -1):
                        return {
                            "indicator": record[0][1],
                            "indicator_value": record[0][2],
                            "entries": [ele for ele in entryList]
                        }, 200
                    else:
                        if (ascending == True):
                            return {
                                "indicator": record[0][1],
                                "indicator_value": record[0][2],
                                "entries": [ele for ele in entryList[:nCountry]]
                            }, 200
                        else:
                            return {
                                "indicator": record[0][1],
                                "indicator_value": record[0][2],
                                "entries": [ele for ele in entryList[-1*nCountry:]]
                            }, 200
                else:
                    return {"message": "Invalid year"}, 404

        except Error:
            return {"message": "Invalid ID"}, 404


# Main function
def main():
    conn = create_connection(db)
    if conn is not None:
        create_table(conn)
        initialize_locationDict(conn)
    else:
        print("Connot create the database connection")


if __name__=="__main__":
    main()
    app.run(debug=True, port=9090)