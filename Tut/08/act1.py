import pandas as pd
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, accuracy_score, recall_score

def load_csv(path):
    df = pd.read_csv(path)

    df = shuffle(df)
    x = df.drop('species', axis=1).values
    y = df['species'].values

    split_point = int(len(x)*0.7)
    x_train = x[:split_point]
    y_train = y[:split_point]
    x_test = x[split_point:]
    y_test = y[split_point:]

    return x_train, y_train, x_test, y_test


def main():
    path = 'iris.csv'
    x_train, y_train, x_test, y_test = load_csv(path)

    knn = KNeighborsClassifier()
    knn.fit(x_train, y_train)

    prediction = knn.predict(x_test)

    print('confusion_matrix:\n', confusion_matrix(y_test, prediction))
    print('precision:\t', precision_score(y_test, prediction, average=None))
    print('recall:\t\t', recall_score(y_test, prediction, average=None))
    print('accuracy:\t', accuracy_score(y_test, prediction))

if __name__ == "__main__":
    main()