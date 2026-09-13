import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

print("🚀 Generating Synthetic Image Data (Zero Download Needed)...")

# 1. Fake Synthetic Images Banana (100 sample images of size 150x150x3)
X_synthetic = np.random.random((100, 150, 150, 3)).astype(np.float32)
y_synthetic = np.random.randint(0, 2, size=(100, 1)) # Binary Labels: 0 or 1

# 2. Build CNN Architecture
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D(2, 2),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='sigmoid') # Binary Classification
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 3. Train Model on Synthetic Data (Fast 2 Epochs)
print("⏳ Training Baseline CNN Model...")
model.fit(X_synthetic, y_synthetic, epochs=2, batch_size=16)

# 4. Save Model File
os.makedirs(r'C:\Users\Hussnain Saifi\Documents\GitHub\CLass-3\Deep_Learning_Projects\Pneumonia_CNN_Project\model', exist_ok=True)
model.save(r'C:\Users\Hussnain Saifi\Documents\GitHub\CLass-3\Deep_Learning_Projects\Pneumonia_CNN_Project\model/pneumonia_cnn_model.h5')
print("✅ SUCCESS: Model saved at '../model/pneumonia_cnn_model.h5' without downloading dataset!")