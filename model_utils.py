import joblib

# Optional SHAP (safe import)
try:
    import shap
    SHAP_AVAILABLE = True
except:
    SHAP_AVAILABLE = False

# Load model
model = joblib.load("model.pkl")

# ---------------- PREDICT ----------------
def predict(data):
    pred = model.predict([data])[0]
    prob = model.predict_proba([data])[0][1]
    return pred, prob

# ---------------- FEATURE IMPORTANCE ----------------
def feature_importance():
    return model.feature_importances_

# ---------------- SHAP EXPLAIN ----------------
def shap_explain(data):
    if not SHAP_AVAILABLE:
        return None, None

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values([data])
    return shap_values, explainer