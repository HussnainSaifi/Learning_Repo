import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import joblib

# 1. Dataset Load / Create Synthetic Data
data = {
    'CreditScore': [619, 608, 502, 699, 850, 645, 822, 376, 501, 684],
    'Age': [42, 41, 42, 39, 43, 44, 50, 29, 44, 27],
    'Tenure': [2, 1, 8, 1, 2, 8, 7, 4, 4, 2],
    'Balance': [0.0, 83807.86, 159660.8, 0.0, 125510.82, 113755.78, 0.0, 115046.74, 142051.07, 134603.88],
    'NumOfProducts': [1, 1, 3, 2, 1, 2, 2, 4, 2, 1],
    'IsActiveMember': [1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
    'EstimatedSalary': [101348.88, 112542.58, 113931.57, 93826.63, 79084.1, 149756.71, 100628.0, 119346.88, 74940.5, 93551.32],
    'Exited': [1, 0, 1, 0, 0, 1, 0, 1, 0, 0] # Target (0 = Stayed, 1 = Churn/Left)
}
df = pd.DataFrame(data)

# 2. Features & Target Split
X = df.drop(columns=['Exited'])
y = df['Exited']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save Scaler
joblib.dump(scaler, r'C:\Users\Hussnain Saifi\Documents\GitHub\CLass-3\Deep_Learning_Projects\ANN_Project\models\scaler.joblib')

# 3. Build Neural Network Architecture
model = Sequential([
    Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.2), # Overfitting control
    Dense(16, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='sigmoid') # Binary Output
])

# Compile Model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# 4. Train Model
model.fit(
    X_train_scaled, 
    y_train, 
    epochs=30, 
    batch_size=16, 
    validation_data=(X_test_scaled, y_test)
)

# Save Model
model.save(r'C:\Users\Hussnain Saifi\Documents\GitHub\CLass-3\Deep_Learning_Projects\ANN_Project\models\churn_ann_model.h5')
print("Scaler aur Model successfully save ho chuke hain!")