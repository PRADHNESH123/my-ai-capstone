#  Customer Churn Predictor — AI Capstone

Predicts whether a telecom customer will churn using Machine Learning.

##  Live Demo
- **Frontend:** https://churn-predictor-pradhnesh.streamlit.app
- **API Docs:** https://my-ai-capstone.onrender.com/docs
- **Health:** https://my-ai-capstone.onrender.com/health

## Local Setup
```bash
git clone https://github.com/PRADHNESH123/my-ai-capstone.git
cd my-ai-capstone
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
streamlit run frontend/app.py
```

##  Docker
```bash
docker build -t churn-api .
docker run -p 8000:8000 churn-api
```

##  API
```bash
curl -X POST https://my-ai-capstone.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"tenure":12,"monthly_charges":65.5,"total_charges":780.0,"contract_type":0}'
```

##  Model
- Algorithm: Random Forest
- Accuracy: ~80%
- Features: tenure, monthly_charges, total_charges, contract_type