import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from config import Config

def get_df():
    filepath = Config.DEFAULT_DATASET
    if not os.path.exists(filepath):
        filepath = os.path.join(Config.BASE_DIR, "Titanic-Dataset.csv")
    return pd.read_csv(filepath)

def ensure_chart_dir():
    os.makedirs(Config.CHARTS_DIR, exist_ok=True)

def style_plot():
    plt.style.use('dark_background')
    fig = plt.gcf()
    fig.patch.set_facecolor('#0f172a')
    ax = plt.gca()
    ax.set_facecolor('#1e293b')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#64748b')
    ax.spines['bottom'].set_color('#64748b')
    ax.tick_params(colors='#94a3b8')
    ax.yaxis.label.set_color('#cbd5e1')
    ax.xaxis.label.set_color('#cbd5e1')

def create_survival_chart():
    ensure_chart_dir()
    df = get_df()
    plt.figure(figsize=(6, 4))
    style_plot()
    
    if "Survived" in df.columns:
        counts = df["Survived"].value_counts()
        colors = ['#ef4444', '#10b981']
        labels = ['Did Not Survive (0)', 'Survived (1)']
        bars = plt.bar([str(x) for x in counts.index], counts.values, color=colors[:len(counts)], width=0.5)
        plt.title("Survival Distribution", color='#f8fafc', fontsize=14, pad=15)
        plt.xlabel("Outcome", color='#cbd5e1')
        plt.ylabel("Passenger Count", color='#cbd5e1')
        plt.xticks([0, 1], labels[:len(counts)])
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 5, int(yval), ha='center', color='#f8fafc', fontweight='bold')
            
    chart_path = os.path.join(Config.CHARTS_DIR, "survival_chart.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=120, facecolor='#0f172a')
    plt.close()
    return "charts/survival_chart.png"

def create_gender_chart():
    ensure_chart_dir()
    df = get_df()
    plt.figure(figsize=(6, 4))
    style_plot()
    
    if "Sex" in df.columns:
        counts = df["Sex"].value_counts()
        colors = ['#3b82f6', '#ec4899']
        bars = plt.bar([str(x).capitalize() for x in counts.index], counts.values, color=colors[:len(counts)], width=0.5)
        plt.title("Gender Distribution", color='#f8fafc', fontsize=14, pad=15)
        plt.xlabel("Gender", color='#cbd5e1')
        plt.ylabel("Count", color='#cbd5e1')
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 5, int(yval), ha='center', color='#f8fafc', fontweight='bold')

    chart_path = os.path.join(Config.CHARTS_DIR, "gender_chart.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=120, facecolor='#0f172a')
    plt.close()
    return "charts/gender_chart.png"

def create_age_histogram():
    ensure_chart_dir()
    df = get_df()
    plt.figure(figsize=(6, 4))
    style_plot()
    
    if "Age" in df.columns:
        age_data = df["Age"].dropna()
        plt.hist(age_data, bins=20, color='#8b5cf6', edgecolor='#0f172a', alpha=0.85)
        plt.title("Age Distribution Histogram", color='#f8fafc', fontsize=14, pad=15)
        plt.xlabel("Age (Years)", color='#cbd5e1')
        plt.ylabel("Frequency", color='#cbd5e1')

    chart_path = os.path.join(Config.CHARTS_DIR, "age_histogram.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=120, facecolor='#0f172a')
    plt.close()
    return "charts/age_histogram.png"

def create_heatmap():
    ensure_chart_dir()
    df = get_df()
    plt.figure(figsize=(7, 5))
    
    num_df = df.select_dtypes(include=[np.number])
    if not num_df.empty:
        corr = num_df.corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, cbar=True)
        plt.title("Correlation Heatmap Matrix", color='#f8fafc', fontsize=14, pad=15)
        plt.xticks(rotation=45, ha='right', color='#cbd5e1')
        plt.yticks(color='#cbd5e1')
    
    chart_path = os.path.join(Config.CHARTS_DIR, "correlation_heatmap.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=120, facecolor='#0f172a')
    plt.close()
    return "charts/correlation_heatmap.png"

def create_box_plot():
    ensure_chart_dir()
    df = get_df()
    plt.figure(figsize=(6, 4))
    style_plot()
    
    if "Fare" in df.columns and "Pclass" in df.columns:
        sns.boxplot(x="Pclass", y="Fare", hue="Pclass", legend=False, data=df, palette="crest")
        plt.title("Fare Distribution by Passenger Class", color='#f8fafc', fontsize=14, pad=15)
        plt.xlabel("Passenger Class (Pclass)", color='#cbd5e1')
        plt.ylabel("Fare ($)", color='#cbd5e1')

    chart_path = os.path.join(Config.CHARTS_DIR, "box_plot.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=120, facecolor='#0f172a')
    plt.close()
    return "charts/box_plot.png"

def generate_all_charts():
    s_chart = create_survival_chart()
    g_chart = create_gender_chart()
    a_chart = create_age_histogram()
    h_chart = create_heatmap()
    b_chart = create_box_plot()
    return {
        "survival": s_chart,
        "gender": g_chart,
        "age": a_chart,
        "heatmap": h_chart,
        "box_plot": b_chart
    }