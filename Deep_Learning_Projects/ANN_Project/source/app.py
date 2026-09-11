from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# App & Model Initialization
app = FastAPI(title="Customer Churn Prediction API")

scaler = joblib.load(r'C:\Users\Hussnain Saifi\Documents\GitHub\CLass-3\Deep_Learning_Projects\ANN_Project\models\scaler.joblib')
model = load_model(r'C:\Users\Hussnain Saifi\Documents\GitHub\CLass-3\Deep_Learning_Projects\ANN_Project\models\churn_ann_model.h5')

# Input Schema Validation
class CustomerInput(BaseModel):
    CreditScore: float
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    IsActiveMember: float
    EstimatedSalary: float

@app.post("/predict")
def predict_churn(customer: CustomerInput):
    # Convert Input to Numpy Array
    data = np.array([[
        customer.CreditScore,
        customer.Age,
        customer.Tenure,
        customer.Balance,
        customer.NumOfProducts,
        customer.IsActiveMember,
        customer.EstimatedSalary
    ]])
    
    # Scale Data
    scaled_data = scaler.transform(data)
    
    # Prediction
    prediction = model.predict(scaled_data)[0][0]
    churn_status = bool(prediction > 0.5)
    
    return {
        "churn_probability": float(prediction),
        "will_churn": churn_status,
        "status_label": "Customer likely to LEAVE" if churn_status else "Customer likely to STAY"
    }