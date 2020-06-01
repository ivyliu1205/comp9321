import pandas as pd
import matplotlib.pyplot as plt

def load_csv(filename):
    return pd.read_csv(filename)

if __name__ == "__main__":
    filename = 'Books.csv'
    df = load_csv(filename)

    number = df['Place of Publication'].value_counts()
    #print(df.to_string())
    number.plot.pie(subplots=True)

    plt.show()