import pandas as pd
from sklearn.utils import shuffle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def load_data(path):
    df = pd.read_csv(path)

    df = shuffle(df)
    x = df.drop('weight6weeks', axis=1).values
    y = df['weight6weeks'].values

    split_point = int(len(x)*0.7)
    x_train = x[:split_point]
    y_train = y[:split_point]
    x_test = x[split_point:]
    y_test = y[split_point:]
    return x_train, y_train, x_test, y_test

if __name__ == "__main__":
    path = 'diet.csv'
    x_train, y_train, x_test, y_test = load_data(path)

    model = LinearRegression().fit(x_train, y_train)

    predication = model.predict(x_test)
    for i in range(len(y_test)):
        print('Expected:', y_test[i], 'Predicted:', predication[i])
    
    print('Mean squared error: %.2f'% mean_squared_error(y_test, predication))