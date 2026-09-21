import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression # 追加: 機械学習モデル

st.title("World Happiness Report - EDA Dashboard")
st.write("データセットの探索的データ分析（EDA）と幸福度の予測シミュレーションを行うダッシュボードです。")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("world_happiness.csv")
    except FileNotFoundError:
        st.warning("CSVファイルが見つからないため、デモ用のデータを生成しています。")
        np.random.seed(42)
        gdp = np.random.uniform(0.5, 2.0, 50)
        score = 3.0 + 2.5 * gdp + np.random.normal(0, 0.5, 50)
        df = pd.DataFrame({
            "Country": [f"Country_{i}" for i in range(1, 51)],
            "Happiness_Score": score,
            "GDP_per_capita": gdp,
            "Social_support": np.random.uniform(0.5, 1.5, 50)
        })
    return df

df = load_data()

st.subheader("1. データセットの確認")
st.dataframe(df.head())

st.subheader("2. 記述統計量 (Descriptive Statistics)")
st.write(df.describe())

st.subheader("3. GDPと幸福度の関係性")
st.scatter_chart(data=df, x="GDP_per_capita", y="Happiness_Score")

# --- ここから下が Step 3 で追加された機械学習セクション ---

st.header("4. 幸福度の予測シミュレーション (Machine Learning)")
st.write("Scikit-learnの回帰モデル(Linear Regression)を用いて、GDPから幸福度を予測します。")

# Prepare data (特徴量Xとターゲットyの準備)
X = df[["GDP_per_capita"]]
y = df["Happiness_Score"]

# Train the model (モデルの学習)
model = LinearRegression()
model.fit(X, y)

# Interactive UI (スライダーでユーザーが値を操作)
st.subheader("GDPを動かして幸福度を予測してみよう")
min_gdp = float(df["GDP_per_capita"].min())
max_gdp = float(df["GDP_per_capita"].max())
mean_gdp = float(df["GDP_per_capita"].mean())

# Create a slider
user_gdp = st.slider("GDP per capita (1人当たりGDP)", min_value=min_gdp, max_value=max_gdp, value=mean_gdp)

# Predict based on user input (ユーザーの入力値をもとに予測)
prediction = model.predict([[user_gdp]])

# Show the result (結果の表示)
st.success(f"予測される幸福度スコア (Predicted Happiness Score): **{prediction[0]:.2f}**")