import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os

# Synthetic dataset banana
np.random.seed(42)
n_samples = 500

industries = ["EdTech", "FinTech", "HealthTech", "FitnessTech", 
              "AI", "E-commerce", "SaaS", "FoodTech", "Sustainability"]

data = {
    "industry": np.random.choice(industries, n_samples),
    "description_length": np.random.randint(50, 500, n_samples),
    "competitor_count": np.random.randint(1, 10, n_samples),
    "feature_count": np.random.randint(2, 8, n_samples),
    "risk_count": np.random.randint(1, 6, n_samples),
}

df = pd.DataFrame(data)

# Label encoder for industry
le = LabelEncoder()
df["industry_encoded"] = le.fit_transform(df["industry"])

# Success score generate karna (rule-based synthetic labels)
df["success_score"] = (
    (df["description_length"] / 500) * 3 +
    (df["feature_count"] / 8) * 3 +
    (1 - df["risk_count"] / 6) * 2 +
    (1 - df["competitor_count"] / 10) * 2
).clip(0, 10).round(1)

# Binary label: 1 if score > 5, 0 otherwise
df["success"] = (df["success_score"] > 5).astype(int)

# Features aur target
X = df[["industry_encoded", "description_length", 
        "competitor_count", "feature_count", "risk_count"]]
y = df["success"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model train karna
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Accuracy check
y_pred = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# Model aur encoder save karna
os.makedirs("app/models_saved", exist_ok=True)
joblib.dump(model, "app/models_saved/success_model.pkl")
joblib.dump(le, "app/models_saved/industry_encoder.pkl")
joblib.dump(industries, "app/models_saved/industries_list.pkl")

print("Model saved successfully!")
print(f"Industries supported: {industries}")