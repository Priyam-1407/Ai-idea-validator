import joblib
import os

# Models load karna
model = joblib.load("app/models_saved/success_model.pkl")
le = joblib.load("app/models_saved/industry_encoder.pkl")
industries_list = joblib.load("app/models_saved/industries_list.pkl")

def predict_success_score(
    industry: str,
    description_length: int,
    competitor_count: int,
    feature_count: int,
    risk_count: int
) -> float:
    # Agar industry known nahi hai, default le lo
    if industry not in industries_list:
        industry = "AI"

    industry_encoded = le.transform([industry])[0]

    features = [[
        industry_encoded,
        description_length,
        competitor_count,
        feature_count,
        risk_count
    ]]

    # Probability predict karna (0-1) → scale to 0-10
    prob = model.predict_proba(features)[0][1]
    score = round(float(prob) * 10, 1)
    return score
