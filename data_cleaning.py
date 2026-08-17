import pandas as pd

def load_and_clean_data():
    
    df = pd.read_csv("data/dataset.csv")

    df.fillna(df.mean(numeric_only=True), inplace=True)

    return df