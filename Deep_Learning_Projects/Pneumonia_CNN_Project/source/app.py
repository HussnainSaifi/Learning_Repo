from fastapi import FastAPI, File, UploadFile
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

app = FastAPI(title="Pneumonia Detection CNN API")

# Load Saved Model
MODEL_PATH = r"C:\Users\Hussnain Saifi\Documents\GitHub\CLass-3\Deep_Learning_Projects\Pneumonia_CNN_Project\model/pneumonia_cnn_model.h5"
model = load_model(MODEL_PATH)

def preprocess_image(image_bytes):
    # Image load karke 150x150 size par convert karna
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((150, 150))
    img_array = np.array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0) # Add batch dimension (1, 150, 150, 3)
    return img_array

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    processed_img = preprocess_image(contents)
    
    prediction = model.predict(processed_img)[0][0]
    is_pneumonia = bool(prediction > 0.5)
    
    return {
        "filename": file.filename,
        "confidence_score": float(prediction),
        "prediction": "PNEUMONIA DETECTED" if is_pneumonia else "NORMAL",
        "status_code": 200
    }