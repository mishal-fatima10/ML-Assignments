"""
Diamond Price Prediction – Streamlit web app
Course: AIC354 Machine Learning Fundamentals (Assignment 3, Task 2)
Student: Mishal Fatima (SP24-BCS-067)

Loads the trained pipeline (diamond_price_model.pkl) created by the notebook and predicts
the price of a diamond from its specifications.
"""
import json
import pickle
from pathlib import Path

import pandas as pd
import streamlit as st

BASE = Path(__file__).parent

st.set_page_config(page_title="Diamond Price Predictor", page_icon="💎", layout="centered")


@st.cache_resource
def load_model():
    with open(BASE / "diamond_price_model.pkl", "rb") as f:
        return pickle.load(f)


@st.cache_data
def load_info():
    with open(BASE / "model_info.json") as f:
        return json.load(f)


@st.cache_data
def load_results():
    return pd.read_csv(BASE / "cv_results.csv")


model = load_model()
info = load_info()
results = load_results()

CUT = info["categories"]["cut"]
COLOR = info["categories"]["color"]
CLARITY = info["categories"]["clarity"]

# ---------------------------------------------------------------- header
st.title("💎 Diamond Price Predictor")
st.caption(
    f"Machine learning model: **{info['best_algorithm']}** · trained on "
    f"{info['n_diamonds']:,} diamonds · chosen from 5 algorithms with "
    f"{info['cv_folds']}-fold cross validation"
)

# ---------------------------------------------------------------- inputs
st.subheader("1. Describe the diamond")

col1, col2 = st.columns(2)
with col1:
    carat = st.number_input("Carat (weight)", min_value=0.2, max_value=5.0, value=0.90, step=0.01)
    cut = st.selectbox("Cut", CUT, index=CUT.index("Ideal"), help="Fair (worst) → Ideal (best)")
with col2:
    color = st.selectbox("Colour", COLOR, index=COLOR.index("G"), help="D (colourless, best) → J (slight tint)")
    clarity = st.selectbox("Clarity", CLARITY, index=CLARITY.index("VS2"), help="I1 (worst) → IF (flawless, best)")

auto_dims = st.checkbox(
    "Estimate the size (x, y, z) automatically from the carat weight",
    value=True,
    help="For a typical round brilliant diamond. Untick to enter measured values in millimetres.",
)

if auto_dims:
    x = round(6.4 * carat ** (1 / 3), 2)      # diameter (mm) of a typical round diamond
    y = x
    z = round(0.615 * x, 2)                   # height (mm)
    depth = round(z / ((x + y) / 2) * 100, 1)
    table = 57.0
    st.caption(f"Estimated: length x = {x} mm, width y = {y} mm, height z = {z} mm, depth = {depth}%, table = {table}%")
else:
    r = info["ranges"]
    c1, c2, c3 = st.columns(3)
    x = c1.number_input("Length x (mm)", 0.1, 12.0, 6.15, 0.01)
    y = c2.number_input("Width y (mm)", 0.1, 60.0, 6.18, 0.01)
    z = c3.number_input("Height z (mm)", 0.1, 35.0, 3.81, 0.01)
    c4, c5 = st.columns(2)
    depth = c4.number_input("Depth (%)", float(r["depth"][0]), float(r["depth"][1]), 61.8, 0.1)
    table = c5.number_input("Table (%)", float(r["table"][0]), float(r["table"][1]), 57.0, 0.1)

# ---------------------------------------------------------------- prediction
st.subheader("2. Predicted price")

if st.button("Predict price", type="primary", width="stretch"):
    features = pd.DataFrame([{
        "carat": carat, "depth": depth, "table": table, "x": x, "y": y, "z": z,
        "cut": cut, "color": color, "clarity": clarity,
    }])
    price = float(model.predict(features)[0])
    price = max(price, 0.0)

    st.metric("Estimated price", f"${price:,.0f}")
    st.info(
        f"Typical error of this model: about **${info['mean_mae']:,.0f}** on average (MAE). "
        f"The RMSE, which punishes large mistakes more, is **${info['mean_rmse']:,.0f}**, and the model explains "
        f"**{info['mean_r2'] * 100:.1f}%** of the variation in diamond prices (R²)."
    )
else:
    st.write("Fill in the form above and press **Predict price**.")

# ---------------------------------------------------------------- model comparison
with st.expander("How was this model chosen? (5-algorithm comparison)"):
    st.write(
        "Five regression algorithms were compared on the **full dataset** with **10-fold cross validation**. "
        "The one with the lowest mean RMSE was trained on all the data and deployed here."
    )
    table_view = results[["Rank", "Algorithm", "Mean RMSE ($)", "Mean MAE ($)", "Mean R2"]].copy()
    st.dataframe(
        table_view.style.format({"Mean RMSE ($)": "${:,.0f}", "Mean MAE ($)": "${:,.0f}", "Mean R2": "{:.4f}"}),
        hide_index=True,
        width="stretch",
    )
    st.bar_chart(results.set_index("Algorithm")["Mean RMSE ($)"], horizontal=True)
    st.caption("Lower RMSE is better.")

st.divider()
st.caption("AIC354 Machine Learning Fundamentals · Assignment 3 · Mishal Fatima (SP24-BCS-067) · COMSATS University Islamabad, Lahore Campus")
