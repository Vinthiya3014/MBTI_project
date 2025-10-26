import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE, RandomOverSampler
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load dataset
df = pd.read_csv("data/merged_dataset.csv")
df.columns = [c.strip() for c in df.columns]

# Fix Q1–Q16
q_cols = [f"Q{i}" for i in range(1, 17)]
df = df.rename(columns={c: c.strip().replace(" ", "") for c in df.columns})

features = q_cols
target = "MBTI"

df = df.dropna(subset=features + [target]).reset_index(drop=True)
df[target] = df[target].str.upper()

# Encode labels
le = LabelEncoder()
y = le.fit_transform(df[target])
X = df[features].astype(float)

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Balance data
try:
    smote = SMOTE(random_state=42, k_neighbors=1)
    X_bal, y_bal = smote.fit_resample(X_scaled, y)
    print("✅ Using SMOTE balancing")
except ValueError as e:
    print(f"⚠️ SMOTE failed: {e}")
    ros = RandomOverSampler(random_state=42)
    X_bal, y_bal = ros.fit_resample(X_scaled, y)

print(f"Original dataset size: {X.shape[0]}")
print(f"Balanced dataset size: {X_bal.shape[0]}")

# Train
clf = RandomForestClassifier(n_estimators=300, random_state=42)
clf.fit(X_bal, y_bal)

# Evaluate
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
y_pred = cross_val_predict(clf, X_bal, y_bal, cv=cv)

acc = accuracy_score(y_bal, y_pred)
print(f"\n✅ Cross-validated Accuracy (balanced): {acc:.2f}\n")
print(classification_report(y_bal, y_pred, target_names=le.classes_))

# Save model artifacts
joblib.dump(clf, "mbti_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(le, "label_encoder.pkl")
print("💾 Saved model, scaler, and encoder!")

# Plot confusion matrix (optional)
cm = confusion_matrix(y_bal, y_pred)
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=le.classes_, yticklabels=le.classes_)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix (Balanced Data)")
plt.show()
