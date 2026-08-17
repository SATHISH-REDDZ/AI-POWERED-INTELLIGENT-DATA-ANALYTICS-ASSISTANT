import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from database import save_accuracy


def train_model():

    df = pd.read_csv("data/dataset.csv")

    df = df.select_dtypes(include=["number"])

    df.fillna(df.mean(), inplace=True)

    X = df.drop("Survived", axis=1)
    y = df["Survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    joblib.dump(
        model,
        "models/trained_model.pkl"
    )

    accuracy = round(accuracy * 100, 2)

    save_accuracy(accuracy)

    return accuracy