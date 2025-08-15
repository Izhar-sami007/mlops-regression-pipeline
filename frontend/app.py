
import os
import requests
import streamlit as st

st.set_page_config(page_title="Regression Predictor", layout="centered")
st.title("🏗️ Regression Predictor (Scikit‑learn)")

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.caption(f"Using API: {API_URL}")

st.write("Enter features (example assumes California Housing: 8 features).")
with st.form("predict_form"):
    feature_str = st.text_input("Comma-separated features", value="8.3, 41.0, 6.9841, 1.0238, 322.0, 2.5555, 37.88, -122.23")
    submitted = st.form_submit_button("Predict")

if submitted:
    try:
        features = [float(x.strip()) for x in feature_str.split(",") if x.strip() != ""]
        payload = {"features": features}
        resp = requests.post(f"{API_URL}/predict", json=payload, timeout=15)
        if resp.ok:
            st.success(f"✅ Prediction: **{resp.json()['prediction']:.4f}**")
        else:
            st.error(f"API error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"Failed: {e}")
