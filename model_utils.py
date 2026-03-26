import joblib
import shap

rf = joblib.load("model.pkl")

def predict(data):
    pred = rf.predict([data])[0]
    prob = rf.predict_proba([data])[0][1]
    return pred, prob

def feature_importance():
    return rf.feature_importances_

def shap_explain(data):
    explainer = shap.TreeExplainer(rf)
    shap_values = explainer.shap_values([data])
    return shap_values, explainer