import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Load CSV Data
data = pd.read_csv("solar_data.csv")

# Rename columns for readability
data = data.rename(columns={"field1": "temperature", "field2": "humidity", "field3": "voltage", "field4": "current"})

# Drop unnecessary columns (Keep only relevant features)
data = data[["temperature", "humidity", "voltage", "current"]]

# **Handle Missing Values**
data = data.dropna()  # Drop rows with NaN values
# OR: Fill NaNs with column mean (Alternative)
# data = data.fillna(data.mean())

# **Generate Efficiency (Synthetic Data)**
data["efficiency"] = (data["voltage"] * data["current"]) / (data["temperature"] + 1)  # Example formula

# Features (X) and Target Variable (y)
X = data[["temperature", "humidity", "voltage", "current"]]
y = data["efficiency"]

# Split Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model (Linear Regression)
model = LinearRegression()
model.fit(X_train, y_train)

# Test Model
y_pred = model.predict(X_test)
error = mean_absolute_error(y_test, y_pred)
print(f"✅ Model Error: {error:.2f}%")

# Save Trained Model
pickle.dump(model, open("solar_efficiency_model.pkl", "wb"))
print("✅ Model Saved Successfully as 'solar_efficiency_model.pkl'!")
