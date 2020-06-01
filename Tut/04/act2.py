import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('iris.csv')
df = df.groupby('species').mean()

df.plot.bar()

plt.show()