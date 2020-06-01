# COMP9321 Assignment3
# Yiting Liu z5211008

import sys
import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error, precision_score, accuracy_score, recall_score
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

ZID = 'z5211008'
SUMMARYONE = 'z5211008.PART1.summary.csv'
OUTPUTONE = 'z5211008.PART1.output.csv'
SUMMARYTWO = 'z5211008.PART2.summary.csv'
OUTPUTTWO = 'z5211008.PART2.output.csv'

# Extract cast_id from cast column
def getCastId(context):
    res = ast.literal_eval(context)
    output = []
    for ele in res:
        output.append(ele['cast_id'])
    output.sort()
    return ','.join(str(e) for e in output)

# Extract crew_id from crew column
def getCrewId(context):
    res = ast.literal_eval(context)
    output = []
    for ele in res:
        output.append(ele['crew_id'])
    output.sort()
    return ','.join(str(e) for e in output)

# Count numbers of item in dictionary
def countNumber(context):
    d = ast.literal_eval(context)
    return len(d)

# < 1980 => 1970, 1980~1990 => 1980, 1990~2000 => 1990, 2000~2010 => 2000, > 2010 => 2010
def divideYear(y):
    if y < 1980: return 1970
    elif y >= 1980 and y < 1990: return 1980
    elif y >= 1990 and y < 2000: return 1990
    elif y >= 2000 and y < 2010: return 2000
    else: return 2010

# nCompany < 0 => 0, nCompany > 12.5 => 13
def arrangeComp(n):
    if n < 1: return 0
    elif n > 12.5: return 13
    else: return n

def extractFirstGenre(d):
    if not d:
        return d
    res = ast.literal_eval(d)
    return res[0]['name']

def divideGenre(s):
    gDict = {"Action":1, "Adventure":2, "Fantasy":3, "Animation":4, "Science Fiction":5, "Drama":6,
            "Thriller":7, "Family":8, "Comedy":9, "History":10, "War":11, "Western":12, "Romance":13, 
            "Crime":14, "Mystery":15, "Horror":16, "Music":17, "Documentary":18 }
    if s in gDict:
        return gDict[s]
    else:
        return 19

# Extract useful data from the original dataframe
def cleanData(df):
    # print(df.info())
    # CAST
    df.cast = df.cast.apply(countNumber)
    # df['female_cast'] = df['cast'].apply(countFemale)
    # df['male_cast'] = df['cast'].apply(countMale)

    # CREW
    df.crew = df.crew.apply(countNumber)
    # df['female_crew'] = df['crew'].apply(countFemale)
    # df['male_crew'] = df['cast'].apply(countMale)
    
    # print('cast', end=' ')
    # print(pd.unique(df.crew))

    # GENRES
    df.genres = df.genres.apply(extractFirstGenre)
    genreList = pd.unique(df.genres)
    df.genres = df.genres.apply(divideGenre)
    # print(genreList)

    # KEYWORDS
    df.keywords = df.keywords.apply(countNumber)

    # COMPANIES
    df.production_companies = df.production_companies.apply(countNumber)
    df.production_companies = df.production_companies.apply(arrangeComp)

    # COUNTRIES
    df.production_countries = df.production_countries.apply(countNumber)
    
    # SPOKEN LANGUAGES
    df.spoken_languages = df.spoken_languages.apply(countNumber)

    # HOMEPAGE
    # No homepage change to 0, has homepage change to 1
    df = df.replace(np.nan, 0)
    df['homepage'] = df['homepage'].apply(lambda x: 1 if x!=0 else 0)
    
    # RUNTIME -- scale runtime between 1 and 0
    df['runtime'] = (df.runtime - df.runtime.min()) / (df.runtime.max() - df.runtime.min())

    # RELEASE_DATE
    df['release_date'] = df['release_date'].str.extract(r'^(\d{4})', expand=False).apply(pd.to_numeric)
    df.release_date = df.release_date.apply(divideYear)

    dropColumns = ['rating', 'original_language', 'original_title', 'overview', 'tagline', 'status']
    df.drop(dropColumns, inplace=True, axis=1)
    
    df = df.drop_duplicates(keep='first')
    # print(df)
    
    # print(df.keywords)
    # print(df['runtime'].max())
    # print(df.iloc[0])
    return df

# Load the data to dataframe for part 1
def load_data_Regression(path):
    df = pd.read_csv(path)
    df = cleanData(df)
    df = shuffle(df)

    # print(df.describe())

    # print(df['revenue'])
    tmp_data = df.values
    idList = [e[0] for e in tmp_data]

    x_data = df.drop(['revenue', 'movie_id'], axis=1).values
    y_data = df['revenue'].values

    return df, idList, x_data, y_data

# Write dataframe to OUT.csv
def writeToOutFile(idList, y_data, y_valid, fileName):
    # print(len(idList))
    # print(len(y_data))
    # print(len(y_valid))
    idList = [int(e) for e in idList]
    tmpDict = {'movie_id': idList, 'revenue': y_valid, 'predicted_revenue': y_data}
    outdf = pd.DataFrame(tmpDict)
    outdf.to_csv(fileName, index=False)

# Calculate data and store it into Summary.csv
def writeToSumFile(vData, pData, fileName):
    msr = round(mean_squared_error(vData, pData), 1)
    coef, p_value = stats.pearsonr(vData, pData)
    tmpDict = {'zid': [ZID], 'MSR': [msr], 'correlation': [round(coef,1)]}
    # print(tmpDict)
    outdf = pd.DataFrame(tmpDict)
    outdf.to_csv(fileName, index=False)

# Used to draw graphs
def drawAndfind(df):
    # ax = df.plot.scatter(x='cast', y='revenue')
    rList = sorted(df['rating'].values)
    nList = [i for i in range(1, len(rList)+1)]
    df.sort_values(by='movie_id')
    # ax = df.plot.scatter(x='movie_id', y='revenue')
    plt.scatter(x=nList, y=rList)
    plt.show()

# Use 
def compareModels(xData, yData, xValid, yValid):
    # Define the models
    model_1 = RandomForestRegressor(n_estimators=600, random_state=0)
    model_2 = RandomForestRegressor(n_estimators=600, min_samples_split=10, random_state=0)
    model_3 = RandomForestRegressor(n_estimators=600, max_depth=20, random_state=0)
    model_4 = RandomForestRegressor(n_estimators=600, min_samples_split=20, random_state=0)
    model_5 = RandomForestRegressor(n_estimators=600, max_depth=10, random_state=0)

    models = [model_1, model_2, model_3, model_4, model_5]
    i = 0
    for model in models:
        model.fit(xData, yData)
        preds = model.predict(xValid)
        print('model ' + str(i))
        print(mean_squared_error(yValid, preds))
        print(stats.pearsonr(yValid, preds))
        i += 1

# Main function for part 1
def solvePartOne(trainPath, testPath):
    traindf, idListTrain, x_train, y_train = load_data_Regression(trainPath)
    validf, idListValid, x_valid, y_valid = load_data_Regression(testPath)
    
    # Feature scaling
    sc = StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_valid = sc.transform(x_valid)

    # drawAndfind(traindf)
    # compareModels(x_train, y_train, x_valid, y_valid)
    
    model = LogisticRegression(random_state=0)
    # model = DecisionTreeRegressor()
    # model = RandomForestRegressor(n_estimators=600, max_depth=10, random_state=0)
    # model = LinearRegression()

    model.fit(x_train, y_train)

    y_pred = model.predict(x_valid)
    
    y_pred = [int(round(e)) for e in y_pred]

    writeToOutFile(idListValid, y_pred, y_valid, fileName=OUTPUTONE)
    writeToSumFile(y_valid, y_pred, fileName=SUMMARYONE)

#################################################
# Divide dataframe to x and y
def arrangeData(df):
    x = df.drop(['revenue', 'rating', 'movie_id'], axis=1).values
    y = df['rating'].values
    return x, y

def solvePartTwo(trainPath, testPath):
    traindf = pd.read_csv(trainPath)
    testdf = pd.read_csv(testPath)

    x_train, y_train = arrangeData(traindf)
    x_valid, y_valid = arrangeData(testdf)



if __name__ == "__main__":
    trainPath, testPath = sys.argv[1], sys.argv[2]
    solvePartOne(trainPath, testPath)
    solvePartTwo(trainPath, testPath)
