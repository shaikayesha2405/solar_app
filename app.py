import requests
from fastapi import FastAPI
import pickle
import numpy as np

# Load trained model
model = pickle.load(open("solar_efficiency_model.pkl", "rb"))

# ThingSpeak Details
THINGSPEAK_WRITE_API_KEY = "KOJWHL7CUSQWTIHE"
THINGSPEAK_CHANNEL_URL = "https://api.thingspeak.com/update?api_key=KOJWHL7CUSQWTIHE&field1=0"

# Constants for Alerts
IDEAL_EFFICIENCY = 85  # Assumed ideal efficiency for comparison
POWER_THRESHOLD = 500  # High power threshold (in Watts) for alerts
LOW_EFFICIENCY_THRESHOLD = 50  # Efficiency below this triggers an alert

# Alert Codes (Numeric Representation)
ALERT_NORMAL = 0
ALERT_LOW_EFFICIENCY = 1
ALERT_HIGH_POWER = 2

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Solar Efficiency Prediction API is Running!"}

@app.get("/predict")
async def predict_efficiency(temperature: float, humidity: float, voltage: float, current: float):
    """Predict efficiency, calculate energy insights, generate alerts, and send data to ThingSpeak."""
    
    # Convert inputs to NumPy array
    input_data = np.array([[temperature, humidity, voltage, current]])
    
    # Predict efficiency
    efficiency = model.predict(input_data)[0]

    # Calculate Power (W) and Energy (Wh) assuming a 1-hour usage interval
    power_watts = voltage * current  # Power in Watts
    energy_wh = power_watts * 1  # Energy in Watt-hours (assuming 1 hour)

    # Energy Savings Calculation (Based on Ideal Efficiency)
    energy_savings = (IDEAL_EFFICIENCY - efficiency) / IDEAL_EFFICIENCY * energy_wh

    # *Generate Numeric Alerts*
    alert_code = ALERT_NORMAL  # Default: No Alert
    if efficiency < LOW_EFFICIENCY_THRESHOLD:
        alert_code = ALERT_LOW_EFFICIENCY  # 1 → Low Efficiency Alert
    elif power_watts > POWER_THRESHOLD:
        alert_code = ALERT_HIGH_POWER  # 2 → High Power Alert

    # Send Data to ThingSpeak
    response = requests.get(
        THINGSPEAK_CHANNEL_URL,
        params={
            "api_key": THINGSPEAK_WRITE_API_KEY,
            "field5": efficiency,  # Predicted Efficiency
            "field6": power_watts,  # Power Consumption
            "field7": energy_savings,  # Energy Savings
            "field8": alert_code  # *Numeric Alert*
        }
    )

    return {
        "predicted_efficiency": efficiency,
        "power_watts": power_watts,
        "energy_wh": energy_wh,
        "energy_savings": energy_savings,
        "alert_code": alert_code,  # Numeric alert instead of text
        "thingspeak_response": response.text
    }