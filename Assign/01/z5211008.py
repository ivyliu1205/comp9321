import ast
import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import re
import random

studentid = os.path.basename(sys.modules[__name__].__file__)

#################################################
# Your personal methods can be here ...
nodatafilter = -10
def load_csv(path):
    return pd.read_csv(path)

def print_dataframe(df, column, row):
    if (column):
        print(','.join(str(col) for col in df))
    
    if (row):
        for index, rows in df.iterrows():
            print(','.join(str(rows[col]) for col in df))

# extact values from one column in a dataframe
def handle_dict_string(df, columnName, dataName, uwantfirstndata):
    # replace all Nan to [{'dataName': 'NaN'}]
    df[columnName] = df[columnName].fillna('[{\''+ dataName +'\': \'NaN\'}]')
    
    # convert string into dictionary
    df[str(columnName)] = df[str(columnName)].apply(ast.literal_eval)

    for index, rows in df.iterrows():
        dataList = []
        # read each item in dict
        for item in rows[columnName]:
            data = item[dataName]
            if (uwantfirstndata == nodatafilter):
                if (data not in dataList):
                    dataList.append(data)
            else:
                if (data not in dataList and len(dataList) < uwantfirstndata):
                    dataList.append(data)
        dataList.sort()
        df.set_value(index, columnName, ','.join(data for data in dataList))
    return df
#################################################


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))
    if other is not None:
        print(question, other)
    if output_df is not None:
        print(output_df.head(5).to_string())


def question_1(movies, credits):
    """
    :param movies: the path for the movie.csv file
    :param credits: the path for the credits.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    moviedf = load_csv(movies)
    creditdf = load_csv(credits)
    df1 = pd.merge(moviedf, creditdf, how='outer', on='id')
    #################################################

    log("QUESTION 1", output_df=df1, other=df1.shape)
    '''
    print(len(creditdf.index))
    print(len(moviedf.index))'''
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df2 = df1.copy()
    keep = ['id', 'title', 'popularity', \
            'cast', 'crew', 'budget',     \
            'genres', 'original_language',\
            'production_companies',       \
            'production_countries',       \
            'release_date', 'revenue',    \
            'runtime', 'spoken_languages',\
            'vote_average', 'vote_count']
    df2.drop(df2.columns.difference(keep), inplace=True, axis=1)
    #################################################

    log("QUESTION 2", output_df=df2, other=(len(df2.columns), sorted(df2.columns)))
    return df2


def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df3 = df2.copy()
    df3.set_index('id', inplace=True)
    #################################################

    log("QUESTION 3", output_df=df3, other=df3.index.name)
    return df3


def question_4(df3):
    """
    :param df3: the dataframe created in question 3
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df4 = df3.copy()
    df4 = df4[~(df4[['budget']] == 0).any(axis=1)]
    #################################################

    log("QUESTION 4", output_df=df4, other=(df4['budget'].min(), df4['budget'].max(), df4['budget'].mean()))
    return df4


def question_5(df4):
    """
    :param df4: the dataframe created in question 4
    :return: df5
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df5 = df4.copy()
    df5.insert(len(df5.columns), 'success_impact', 0)
    
    df5['success_impact'] = (df5['revenue'] - df5['budget']) / df5['budget']
    #################################################

    log("QUESTION 5", output_df=df5,
        other=(df5['success_impact'].min(), df5['success_impact'].max(), df5['success_impact'].mean()))
    return df5


def question_6(df5):
    """
    :param df5: the dataframe created in question 5
    :return: df6
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df6 = df5.copy()
    max_value = df6['popularity'].max()
    min_value = df6['popularity'].min()
    df6['popularity'] =  ((df6['popularity'] - min_value)/((max_value - min_value) / 100))
    #################################################

    log("QUESTION 6", output_df=df6, other=(df6['popularity'].min(), df6['popularity'].max(), df6['popularity'].mean()))
    return df6


def question_7(df6):
    """
    :param df6: the dataframe created in question 6
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df7 = df6.copy()
    df7['popularity'] = df7['popularity'].fillna(0).astype('int16')
    #################################################

    log("QUESTION 7", output_df=df7, other=df7['popularity'].dtype)
    return df7


def question_8(df7):
    """
    :param df7: the dataframe created in question 7
    :return: df8
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    
    #################################################
    # Your code goes here ...
    df8 = df7.copy()
    
    df8 = handle_dict_string(df8, 'cast', 'character', nodatafilter)

    #################################################

    log("QUESTION 8", output_df=df8, other=df8["cast"].head(10).values)
    return df8


def question_9(df8):
    """
    :param df9: the dataframe created in question 8
    :return: movies
            Data Type: List of strings (movie titles)
            Please read the assignment specs to know how to create the output
    """

    #################################################
    # Your code goes here ...
    df9 = df8.copy()
    movies = []

    df9.insert(len(df9.columns), 'num_of_character', 0)
    df9['num_of_character'] = df9['cast'].str.count(',') + 1
    newdf = df9.nlargest(10, 'num_of_character')

    for index, rows in newdf.iterrows():
        movies.append(rows['title'])
    #################################################

    log("QUESTION 9", output_df=None, other=movies)
    return movies


def question_10(df8):
    """
    :param df8: the dataframe created in question 8
    :return: df10
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df10 = df8.copy()
    # add a new column to store datetime format of release_date
    df10['new_release_date'] = pd.to_datetime(df10.release_date)
    df10.sort_values(by=['new_release_date'], inplace=True, ascending=False)
    
    del df10['new_release_date']
    #################################################

    log("QUESTION 10", output_df=df10, other=df10["release_date"].head(5).to_string().replace("\n", " "))
    return df10


def question_11(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    df11 = df10.copy()

    df11 = handle_dict_string(df11, 'genres', 'name', nodatafilter)

    # Select part of df11 to make faster
    df11_plot = pd.DataFrame(df11['genres'])

    # split the rows by different type of genres
    df11_plot = pd.concat([pd.Series(row['genres'].split(',')) for _, row in df11_plot.iterrows()]).reset_index()
    df11_plot.columns = ['index', 'genres']
    
    # drop the rows with 'NaN' in genres
    df11_plot = df11_plot.query('genres != "NaN"')

    # Label 'Music', 'Western', 'TV Movie' and 'Documentary' to 'other genres'
    needtoChange = ['Documentary', 'Music', 'TV Movie', 'Western']
    df11_plot['genres'] = df11_plot['genres'].apply(lambda x: 'other genres\n(Documentary,Music,TV Movie,Western)' if x in needtoChange else x)

    ngenres = df11_plot['genres'].value_counts()
    ngenres.plot.pie(autopct='%1.1f%%', pctdistance=1.6, subplots=True)
    #plt.show()
    #################################################

    plt.savefig("{}-Q11.png".format(studentid))


def question_12(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    df12 = df10.copy()
    
    df12 = handle_dict_string(df12, 'production_countries', 'name', nodatafilter)

    # Select part of df12 to make faster
    df12_plot = pd.DataFrame(df12['production_countries'])

    # drop the rows with 'NaN' in production_countries
    df12_plot = df12_plot.query('production_countries != "NaN"')

    # split the rows by different type of genres
    df12_plot = pd.concat([pd.Series(row['production_countries'].split(',')) for _, row in df12_plot.iterrows()]).reset_index()
    df12_plot.columns = ['index', 'production_countries']
    
    df12_plot = df12_plot.groupby('production_countries').count()
    df12_plot.sort_values(['production_countries'], inplace=True)
    df12_plot.columns = ['production_countries']
    
    axes = df12_plot.plot.bar(legend=False, subplots=True)
    plt.title('Production Country')
    for ax in axes:
        for p in ax.patches:
            height = p.get_height()
            x, y = p.get_xy()
            ax.annotate('{}'.format(height), (x, y + height))
    #plt.show()
    #################################################

    plt.savefig("{}-Q12.png".format(studentid))


def question_13(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    df13 = df10.copy()
    
    # Select part of df11 to make faster
    df13_plot = pd.DataFrame(df13[['vote_average', 'success_impact', 'spoken_languages']])
    
    # Handle with the 'spoken_languages' column, and choose the first language for multiple-language movies
    df13_plot = handle_dict_string(df13_plot, 'spoken_languages', 'name', 1)
    
    # select the rows with non 'NaN' in both columns of 'vote_average' and 'success_impact'
    df13_plot = df13_plot.query('vote_average != "NaN" and success_impact != "NaN"')
    
    # plot a scatter chart
    df13_plot = pd.DataFrame(dict(x=df13_plot['vote_average'], y=df13_plot['success_impact'], languages=df13_plot['spoken_languages']))
    groups = df13_plot.groupby('languages')
    
    fig, ax = plt.subplots()
    # using different markers to prevent repeating
    markers = ["1" ,"p", "d", "x" , "o" , "v" , "^" , "<", ">", "*", "s", "h" ,"+"]
    for language, group in groups:
        ax.plot(group.x, group.y, marker=random.choice(markers), linestyle='', label=language)
        
    ax.legend(ncol=3, prop={'size': 7})
    #print(df13_plot.to_string())
    #ax = df13_plot.plot.scatter(x='vote_average', y='success_impact')
    plt.xlabel('vote_average')
    plt.ylabel('impact_success')
    plt.title('vote_average vs. impact_success')
    #plt.show()
    #################################################

    plt.savefig("{}-Q13.png".format(studentid))


if __name__ == "__main__":
    df1 = question_1("movies.csv", "credits.csv")
    df2 = question_2(df1)
    df3 = question_3(df2)
    df4 = question_4(df3)
    df5 = question_5(df4)
    df6 = question_6(df5)
    df7 = question_7(df6)
    df8 = question_8(df7)
    movies = question_9(df8)
    df10 = question_10(df8)
    question_11(df10)
    question_12(df10)
    question_13(df10)