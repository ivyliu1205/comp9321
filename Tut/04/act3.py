import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_csv('iris.csv')

    sdf = df.query('species == "setosa"')
    vdf = df.query('species == "versicolor"')
    vidf = df.query('species == "virginica"')

    ax = sdf.plot.scatter(x='sepal_length', y='sepal_width', label='setosa')
    ax = vdf.plot.scatter(x='sepal_length', y='sepal_width', label='versicolor', color='blue', ax=ax)
    ax = vidf.plot.scatter(x='sepal_length', y='sepal_width', label='virginica', color='brown', ax=ax)

    ax = sdf.plot.scatter(x='petal_length', y='petal_width', label='setosa')
    ax = vdf.plot.scatter(x='petal_length', y='petal_width', label='versicolor', color='blue', ax=ax)
    ax = vidf.plot.scatter(x='petal_length', y='petal_width', label='virginica', color='brown', ax=ax)

    plt.show()