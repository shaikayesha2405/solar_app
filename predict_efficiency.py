import pickle
import numpy as np

# Load the trained model
model = pickle.load(open("solar_efficiency_model.pkl", "rb"))

# Example input (temperature, humidity, voltage, current)
new_data = np.array([[30, 60, 12.5, 3.2]])  # Replace with real sensor values

# Predict Efficiency
predicted_efficiency = model.predict(new_data)

print(f"🔹 Predicted Solar Efficiency: {predicted_efficiency[0]:.2f}%")