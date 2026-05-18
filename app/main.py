# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from pathlib import Path
import joblib
import numpy as np

# ── App instance ──────────────────────────────────────────
app = FastAPI(
    title="Churn Predictor API",
    description="Predicts whether a telecom customer will churn",
    version="1.0.0"
)

# ── Load model once at startup ────────────────────────────
MODEL_PATH = Path(__file__).parent.parent / "model" / "churn_pipeline.pkl"

try:
    pipeline = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    pipeline = None

# ── Input schema ──────────────────────────────────────────
class ChurnInput(BaseModel):
    tenure: int
    monthly_charges: float
    total_charges: float
    contract_type: int  # 0=Month-to-month, 1=One year, 2=Two year

    @field_validator('tenure')
    def tenure_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('tenure must be 0 or greater')
        return v

    @field_validator('monthly_charges', 'total_charges')
    def charges_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('charges must be 0 or greater')
        return v

    @field_validator('contract_type')
    def contract_must_be_valid(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError('contract_type must be 0, 1, or 2')
        return v

# ── Output schema ─────────────────────────────────────────
class ChurnOutput(BaseModel):
    churn: bool
    probability: float
    confidence: str
    message: str

# ── Endpoints ─────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": pipeline is not None
    }

@app.post("/predict", response_model=ChurnOutput)
def predict(data: ChurnInput):

    # Check model is loaded
    if pipeline is None:
        raise HTTPException(
            status_code=500,
            detail="Model not loaded. Check server logs."
        )

    # Prepare input array
    X = np.array([[
        data.tenure,
        data.monthly_charges,
        data.total_charges,
        data.contract_type
    ]])

    # Run inference
    prediction = pipeline.predict(X)[0]
    probability = pipeline.predict_proba(X)[0][1]

    # Confidence label
    if probability > 0.75 or probability < 0.25:
        confidence = "High"
    elif probability > 0.60 or probability < 0.40:
        confidence = "Medium"
    else:
        confidence = "Low"

    # Human readable message
    if prediction == 1:
        message = f"Customer is likely to churn ({probability:.0%} probability)"
    else:
        message = f"Customer is likely to stay ({(1-probability):.0%} probability)"

    return ChurnOutput(
        churn=bool(prediction),
        probability=round(float(probability), 3),
        confidence=confidence,
        message=message
    )

# ── Root endpoint ─────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "Churn Predictor API is running!",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict"
    }