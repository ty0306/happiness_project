import streamlit as st
import requests

st.title("Well-being Digital Twin Dashboard")
st.write("マクロな統計データと、個人の生理的データ（心拍変動・内受容感覚）を掛け合わせて幸福度を予測するデジタルツインのプロトタイプです。")

st.header("1. Digital Twin Parameters")
st.write("ウェアラブルデバイス等から取得される生理心理学的な指標をシミュレーションします。")

# 3つのスライダーを横並びに配置
col1, col2, col3 = st.columns(3)
with col1:
    user_gdp = st.slider("GDP (マクロ経済)", 0.5, 2.0, 1.2)
with col2:
    user_hrv = st.slider("HRV (心拍変動)", 20.0, 100.0, 60.0, help="ストレスが低いと高くなる傾向があります")
with col3:
    user_intero = st.slider("Interoception (内受容感覚)", 0.0, 1.0, 0.5, help="自身の身体の内部状態を正確に知覚する能力")

st.header("2. Predict Well-being Score")

if st.button("デジタルツインによる幸福度予測を実行 (Run Prediction)"):
    API_URL = "http://127.0.0.1:8000/predict/"
    # 3つのパラメータをバックエンドに送信
    payload = {
        "gdp": user_gdp,
        "hrv": user_hrv,
        "interoception": user_intero
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"予測される個人のウェルビーイングスコア: **{result['predicted_score']:.2f}**")
        else:
            st.error("APIからエラーが返されました。")
    except requests.exceptions.ConnectionError:
        st.error("APIサーバーに接続できません。裏側でFastAPIが起動しているか確認してください。")