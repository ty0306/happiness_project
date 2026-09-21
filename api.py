from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

app = FastAPI(title="Digital Twin Well-being API")

# 1. デジタルツイン用の疑似データを生成（生理心理学の指標を追加）
np.random.seed(42)
gdp = np.random.uniform(0.5, 2.0, 50)
# 心拍変動 (HRV): リラックス状態の指標として 20〜100 の値
hrv = np.random.uniform(20.0, 100.0, 50)
# 内受容感覚 (Interoceptive Accuracy): 身体感覚の鋭敏さを 0.0〜1.0 のスコアで表現
interoception = np.random.uniform(0.1, 0.9, 50)

# 3つの変数がそれぞれ幸福度に寄与すると仮定した計算式
score = 2.0 + (1.5 * gdp) + (0.02 * hrv) + (1.0 * interoception) + np.random.normal(0, 0.3, 50)

df = pd.DataFrame({
    "GDP": gdp, 
    "HRV": hrv, 
    "Interoception": interoception, 
    "Happiness_Score": score
})

# 2. 重回帰モデルの学習（3つの特徴量を使用）
model = LinearRegression()
model.fit(df[["GDP", "HRV", "Interoception"]], df["Happiness_Score"])

# 3. リクエストのデータ型を拡張
class PredictRequest(BaseModel):
    gdp: float
    hrv: float
    interoception: float

# 4. エンドポイント
@app.post("/predict/")
def predict_happiness(request: PredictRequest):
    # 3つの入力値から予測を実行
    prediction = model.predict([[request.gdp, request.hrv, request.interoception]])
    return {"predicted_score": float(prediction[0])}