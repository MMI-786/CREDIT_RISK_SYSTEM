import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    roc_curve,
    auc
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data.csv")   # 👉 make sure your dataset name is correct

# ---------------- FEATURES & TARGET ----------------
# 👉 Change 'target' to your actual column name if needed
X = df.drop("target", axis=1)
y = df["target"]

# ---------------- TRAIN TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y   # 🔥 important for balanced split
)

# ---------------- MODELS ----------------
lr = LogisticRegression(max_iter=1000)
rf = RandomForestClassifier(n_estimators=100, random_state=42)

# ---------------- TRAIN ----------------
lr.fit(X_train, y_train)
rf.fit(X_train, y_train)

# ---------------- PREDICT ----------------
lr_pred = lr.predict(X_test)
rf_pred = rf.predict(X_test)

# ---------------- ACCURACY ----------------
lr_acc = accuracy_score(y_test, lr_pred)
rf_acc = accuracy_score(y_test, rf_pred)

print(f"\n📊 Logistic Regression Accuracy: {round(lr_acc, 4)}")
print(f"📊 Random Forest Accuracy: {round(rf_acc, 4)}")

# ---------------- CLASSIFICATION REPORT ----------------
print("\n🔍 Logistic Regression Report:")
print(classification_report(y_test, lr_pred))

print("\n🔍 Random Forest Report:")
print(classification_report(y_test, rf_pred))

# ---------------- SELECT BEST MODEL ----------------
if rf_acc > lr_acc:
    best_model = rf
    print("\n✅ Random Forest selected as best model")
else:
    best_model = lr
    print("\n✅ Logistic Regression selected as best model")

# ---------------- SAVE MODEL ----------------
joblib.dump(best_model, "model.pkl")
print("💾 Model saved as model.pkl")

# ---------------- ROC CURVE ----------------
# Use probability scores
y_prob = best_model.predict_proba(X_test)[:, 1]

fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {round(roc_auc, 3)}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

plt.savefig("roc_curve.png")
plt.close()

print("📈 ROC curve saved as roc_curve.png")