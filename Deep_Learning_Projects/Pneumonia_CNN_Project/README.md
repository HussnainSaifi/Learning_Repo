
# 🫁 Pneumonia Detection CNN API

An end-to-end Computer Vision and REST API service built with **TensorFlow/Keras** and **FastAPI**. This project extracts visual features from Chest X-Ray images using Convolutional Neural Networks (CNN) to classify images as either **NORMAL** or **PNEUMONIA**.

---

## 🚀 Key Features

* **CNN Architecture:** Custom Convolutional Neural Network with `Conv2D`, `MaxPooling2D`, `Dropout`, and `Dense` layers.
* **FastAPI Backend:** Lightweight REST API endpoint for real-time image inference.
* **Data Normalization:** Automated image resizing ($150 \times 150$) and pixel scaling ($0.0 - 1.0$).
* **Swagger Interactive Docs:** Pre-built testing UI available via `/docs`.

---

## 🛠️ Project Structure

```text
pneumonia-cnn-api/
│
├── models/                  # Saved Trained CNN Model (.h5)
│   └── pneumonia_cnn_model.h5
│
├── src/
│   ├── train.py             # Synthetic/Real Dataset Generator & Training Script
│   └── app.py               # FastAPI Server for Model Inference
│
├── requirements.txt         # Dependencies
└── README.md                # Project Documentation
```
