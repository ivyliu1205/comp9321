import pandas as pd
from sklearn.utils import shuffle
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def load_data(path):
    df = pd.read_csv(path)

    df = shuffle(df)
    df_without_label = df.drop('species', axis=1)
    return df, df_without_label

if __name__=="__main__":
    path = 'iris.csv'

    df, df_without_label = load_data(path)

    estimator = KMeans(n_clusters=3)
    estimator.fit(df_without_label)

    labels = estimator.labels_
    df['cluster'] = pd.Series(labels, index=df.index)

    print(labels)

    cluster_0 = df.query('cluster == 0')
    cluster_1 = df.query('cluster == 1')
    cluster_2 = df.query('cluster == 2')

    fig, axes = plt.subplots(nrows=1, ncols=1)
    fig.set_size_inches(18.5, 10.5)
    fig.tight_layout()

    ax = cluster_0.plot.scatter(x='petal_length', y='petal_width', label='Cluster-0', color='red', ax=axes)
    ax = cluster_1.plot.scatter(x='petal_length', y='petal_width', label='Cluster-1', color='green', ax=ax)
    ax = cluster_2.plot.scatter(x='petal_length', y='petal_width', label='Cluster-2', color='blue', ax=ax)

    for i, label in enumerate(df['species']):
    
        label = label[0:4]
        ax.annotate(label, (list(df['petal_length'])[i], list(df['petal_width'])[i]), color='gray', fontSize=9,
                    horizontalalignment='left',
                    verticalalignment='bottom')

    plt.show()