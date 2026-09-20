import streamlit as st
import pandas as pd
import numpy as np

# Set the title of the dashboard
st.title("World Happiness Report - EDA Dashboard")
st.write("データセットの探索的データ分析（EDA）を行うダッシュボードです。")

@st.cache_data
def load_data():
    try:
        # Load the actual CSV file if it exists
        df = pd.read_csv("world_happiness.csv")
    except FileNotFoundError:
        # CSVがない場合でもアプリが動くよう、相関を持たせたダミーデータを生成
        st.warning("CSVファイルが見つからないため、デモ用のデータを生成しています。")
        np.random.seed(42)
        gdp = np.random.uniform(0.5, 2.0, 50)
        # 疑似的な回帰モデルによる幸福度スコアの生成
        score = 3.0 + 2.5 * gdp + np.random.normal(0, 0.5, 50)
        df = pd.DataFrame({
            "Country": [f"Country_{i}" for i in range(1, 51)],
            "Happiness_Score": score,
            "GDP_per_capita": gdp,
            "Social_support": np.random.uniform(0.5, 1.5, 50)
        })
    return df

# Load the dataset
df = load_data()

# 1. Raw Data Display
st.subheader("1. データセットの確認")
st.dataframe(df.head())

# 2. Descriptive Statistics (記述統計量)
st.subheader("2. 記述統計量 (Descriptive Statistics)")
st.write(df.describe())

# 3. Correlation Scatter Plot (相関の可視化)
st.subheader("3. GDPと幸福度の関係性")
st.scatter_chart(data=df, x="GDP_per_capita", y="Happiness_Score")