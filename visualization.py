import pandas as pd
import matplotlib.pyplot as plt


def create_survival_chart():

    df = pd.read_csv("data/dataset.csv")

    plt.figure(figsize=(6,4))

    df["Survived"].value_counts().plot(kind="bar")

    plt.title("Survival Distribution")

    plt.savefig("app/static/charts/survival_chart.png")

    plt.close()


def create_gender_chart():

    df = pd.read_csv("data/dataset.csv")

    plt.figure(figsize=(6,4))

    df["Sex"].value_counts().plot(kind="bar")

    plt.title("Gender Distribution")

    plt.savefig("app/static/charts/gender_chart.png")

    plt.close()


def create_age_histogram():

    df = pd.read_csv("data/dataset.csv")

    plt.figure(figsize=(6,4))

    df["Age"].hist()

    plt.title("Age Distribution")

    plt.savefig("app/static/charts/age_histogram.png")

    plt.close()


def create_heatmap():

    df = pd.read_csv("data/dataset.csv")

    corr = df.select_dtypes(include="number").corr()

    plt.figure(figsize=(8,6))

    plt.imshow(corr)

    plt.colorbar()

    plt.title("Correlation Heatmap")

    plt.savefig("app/static/charts/correlation_heatmap.png")

    plt.close()