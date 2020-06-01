# COMP9321 Assignment3
# Yiting Liu z5211008

import sys
import ast
import operator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error, average_precision_score, accuracy_score, recall_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

ZID = 'z5211008'
SUMMARYONE = 'z5211008.PART1.summary.csv'
OUTPUTONE = 'z5211008.PART1.output.csv'
SUMMARYTWO = 'z5211008.PART2.summary.csv'
OUTPUTTWO = 'z5211008.PART2.output.csv'

# Write outputs to output file
def writeToOutput(idList, pred, partOne):
    tmpList = list(zip(idList, pred))
    tmpList.sort(key=operator.itemgetter(0))
    otherList = list(zip(*tmpList))
    idList = otherList[0]
    pred = [int(round(e, 0)) for e in pred]
    # Part One
    if partOne:
        tmpDict = {"movie_id": idList, "predicted_revenue": pred}
        outdf = pd.DataFrame(tmpDict)
        outdf.to_csv(OUTPUTONE, index=False)
    # Part Two
    else:
        tmpDict = {"movie_id": idList, "predicted_rating": pred}
        outdf = pd.DataFrame(tmpDict)
        outdf.to_csv(OUTPUTTWO, index=False)

# Write summary to summary file
def writeToSummary(pred, valid, partOne):
    # Part One
    if partOne:
        msr = round(mean_squared_error(valid, pred), 2)
        coef, p_value = stats.pearsonr(valid, pred)
        tmpDict = {'zid': [ZID], 'MSR': [msr], 'correlation': [round(coef,2)]}
        # print(tmpDict)
        outdf = pd.DataFrame(tmpDict)
        outdf.to_csv(SUMMARYONE, index=False)
    # Part Two
    else:
        # print(pred)
        classList = list(set(pred))
        # print(classList)
        prec, recall = 0, 0
        for n in classList:
            prec += average_precision_score(valid, pred, pos_label=n)
            recall += recall_score(valid, pred, pos_label=n)
        avgPrec = prec/len(classList)
        avgRecall = recall/len(classList)
        accuracy = accuracy_score(valid, pred)
        tmpDict = {'zid': [ZID], 'average_precision': [round(avgPrec, 2)], 'average_recall': [round(avgRecall, 2)], 'accuracy': [round(accuracy, 2)]}
        outdf = pd.DataFrame(tmpDict)
        outdf.to_csv(SUMMARYTWO, index=False)

# Choose models and make predictions, return y_pred
def makePrediction(x, y, xValid, partOne):
    if partOne:
        model = RandomForestRegressor(n_estimators=90, max_depth=10, random_state=0)
        model.fit(x, y)
        pred = model.predict(xValid)
        return pred
    else:
        model = KNeighborsClassifier(n_neighbors=45)
        model.fit(x, y)
        pred = model.predict(xValid)
        return pred

# Split the dataframe into x and y
def extractData(df, partOne):
    # Part one
    if partOne:
        x = df.drop(['movie_id', 'rating', 'revenue'], axis=1).values
        y = df['revenue'].values
    # Part two
    else:
        x = df.drop(['movie_id', 'rating', 'revenue'], axis=1).values
        y = df['rating'].values
    return x, y

# Data visualization
def drawData(df):
    pass

def countNum(s):
    d = ast.literal_eval(s)
    return len(d)

def extractFirstGenre(d):
    if not d:
        return d
    res = ast.literal_eval(d)
    return res[0]['name']

# Clean data
def cleandfOne(df):
    # cast
    # df['cast'] = df['cast'].apply(countNum)
    
    # crew
    # df['crew'] = df['crew'].apply(countNum)

    # budget
    # genres
    df.genres = df.genres.apply(extractFirstGenre)
    encoder = LabelEncoder()
    df.genres = encoder.fit_transform(df.genres.values)

    # homepage
    df = df.replace(np.nan, 0)
    df['homepage'] = df['homepage'].apply(lambda x: 1 if x!=0 else 0)
    
    # production_companies
    df['production_companies'] = df['production_companies'].apply(countNum)
    
    # production_countries
    df['production_countries'] = df['production_countries'].apply(countNum)
    
    # release_date
    df['release_date'] = df['release_date'].str.extract(r'^(\d{4})', expand=False).apply(pd.to_numeric)
    # print(df['release_date'])

    # runtime
    df['runtime'] = (df.runtime - df.runtime.min()) / (df.runtime.max() - df.runtime.min())

    dropColumns = ['crew', 'cast', 'tagline', 'status', 'overview', 'spoken_languages', 'original_language', 'original_title', 'keywords']
    df.drop(dropColumns, inplace=True, axis=1)

    # print(df.info())
    return df

def cleandfTwo(df):
    # cast
    df['cast'] = df['cast'].apply(countNum)
    
    # crew
    df['crew'] = df['crew'].apply(countNum)

    # budget
    # genres
    df.genres = df.genres.apply(extractFirstGenre)
    encoder = LabelEncoder()
    df.genres = encoder.fit_transform(df.genres.values)

    # homepage
    df = df.replace(np.nan, 0)
    df['homepage'] = df['homepage'].apply(lambda x: 1 if x!=0 else 0)
    
    # production_companies
    df['production_companies'] = df['production_companies'].apply(countNum)
    
    # production_countries
    df['production_countries'] = df['production_countries'].apply(countNum)
    
    # release_date
    df['release_date'] = df['release_date'].str.extract(r'^(\d{4})', expand=False).apply(pd.to_numeric)
    # runtime
    df['runtime'] = (df.runtime - df.runtime.min()) / (df.runtime.max() - df.runtime.min())
    # spoken_languages

    dropColumns = ['keywords', 'original_language', 'original_title', 'tagline', 'status', 'overview', 'spoken_languages']
    df.drop(dropColumns, inplace=True, axis=1)

    # print(df.info())
    return df
#####################################
# Main functions
def solvePartOne(trainPath, testPath):
    traindf = pd.read_csv(trainPath)
    validf = pd.read_csv(testPath)

    traindf = cleandfOne(traindf)
    validf = cleandfOne(validf)

    drawData(traindf)

    x_train, y_train = extractData(traindf, partOne=True)
    x_valid, y_valid = extractData(validf, partOne=True)

    y_pred = makePrediction(x_train, y_train, x_valid, partOne=True)

    idList = validf['movie_id'].values
    idList = [int(e) for e in idList]

    writeToOutput(idList, y_pred, partOne = True)
    writeToSummary(y_pred, y_valid, partOne = True)

def solvePartTwo(trainPath, testPath):
    traindf = pd.read_csv(trainPath)
    validf = pd.read_csv(testPath)
    # print(validf.rating.unique())
    traindf = cleandfTwo(traindf)
    validf = cleandfTwo(validf)
    
    drawData(traindf)

    x_train, y_train = extractData(traindf, partOne=False)
    x_valid, y_valid = extractData(validf, partOne=False)

    y_pred = makePrediction(x_train, y_train, x_valid, partOne=False)

    idList = validf['movie_id'].values
    idList = [int(e) for e in idList]

    writeToOutput(idList, y_pred, partOne = False)
    writeToSummary(y_pred, y_valid, partOne = False)

if __name__ == "__main__":
    trainPath, testPath = sys.argv[1], sys.argv[2]
    solvePartOne(trainPath, testPath)
    solvePartTwo(trainPath, testPath)

