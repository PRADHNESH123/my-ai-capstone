# frontend/app.py

import streamlit as st
import requests

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="Churn Predictor",
    page_icon="📊",
    layout="centered"
)

# ── API URL ───────────────────────────────────────────────
import os
API_URL = os.getenv("API_URL", "https://my-ai-capstone.onrender.com/predict")

# ── Header ────────────────────────────────────────────────
st.title("📊 Customer Churn Predictor")
st.markdown("Enter customer details below to predict whether they will churn.")
st.divider()

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.header("ℹ️ About")
    st.write("This app predicts telecom customer churn using a Random Forest model.")
    st.divider()
    st.subheader("📌 Contract Types")
    st.write("**0** → Month-to-month")
    st.write("**1** → One year")
    st.write("**2** → Two year")
    st.divider()
    st.subheader("🎯 Model Info")
    st.write("Algorithm: Random Forest")
    st.write("Accuracy: ~80%")
    st.write("Features: 4")

# ── Input form ────────────────────────────────────────────
st.subheader("Customer Details")

col1, col2 = st.columns(2)

with col1:
    tenure = st.number_input(
        "Tenure (months)",
        min_value=0,
        max_value=120,
        value=12,
        help="How long the customer has been with the company"
    )
    total_charges = st.number_input(
        "Total Charges ($)",
        min_value=0.0,
        max_value=10000.0,
        value=780.0,
        step=10.0,
        help="Total amount charged to the customer"
    )

with col2:
    monthly_charges = st.number_input(
        "Monthly Charges ($)",
        min_value=0.0,
        max_value=500.0,
        value=65.5,
        step=0.5,
        help="Amount charged monthly"
    )
    contract_type = st.selectbox(
        "Contract Type",
        options=[0, 1, 2],
        format_func=lambda x: {
            0: "Month-to-month",
            1: "One year",
            2: "Two year"
        }[x],
        help="Type of customer contract"
    )

st.divider()

# ── Predict button ────────────────────────────────────────
if st.button("🔍 Predict Churn", use_container_width=True, type="primary"):

    payload = {
        "tenure": tenure,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "contract_type": contract_type
    }

    with st.spinner("Analyzing customer data..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)

            # ── Handle validation error ────────────────
            if response.status_code == 422:
                st.error("❌ Invalid input — please check your values and try again.")

            # ── Handle server error ────────────────────
            elif response.status_code == 500:
                st.error("❌ Server error — the model may not be loaded correctly.")

            # ── Success ───────────────────────────────
            elif response.status_code == 200:
                result = response.json()

                st.divider()
                st.subheader("📈 Prediction Result")

                # Main result
                if result['churn']:
                    st.error(f"⚠️ This customer is **likely to CHURN**")
                else:
                    st.success(f"✅ This customer is **likely to STAY**")

                # Metrics row
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        label="Churn Probability",
                        value=f"{result['probability']:.0%}"
                    )
                with col2:
                    st.metric(
                        label="Retention Probability",
                        value=f"{1 - result['probability']:.0%}"
                    )
                with col3:
                    st.metric(
                        label="Confidence",
                        value=result['confidence']
                    )

                # Probability bar
                st.write("**Churn Risk Level:**")
                st.progress(result['probability'])

                # Message
                st.info(f"💬 {result['message']}")

            else:
                st.error(f"Unexpected error: {response.status_code}")

        # ── Connection errors ──────────────────────────
        except requests.exceptions.ConnectionError:
            st.warning("⚠️ Cannot reach the API. Make sure the backend is running on port 8000.")
            st.code("uvicorn app.main:app --reload --port 8000", language="bash")

        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The server may be busy — try again.")

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

# ── Footer ────────────────────────────────────────────────
st.divider()
st.caption("Built with FastAPI + Streamlit | Capstone Project")