import requests
import pandas as pd

CHANNEL_ID = "2850348"
READ_API_KEY = "33QW2MRE0NIQ9S68"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for HTTP issues

    # Write CSV file with UTF-8 encoding
    with open("solar_data.csv", "w", encoding="utf-8") as file:
        file.write(response.text)

    print("✅ Data downloaded successfully and saved as solar_data.csv!")

    # Read and display first 5 rows
    df = pd.read_csv("solar_data.csv")
    print(df.head())

except requests.exceptions.RequestException as e:
    print("❌ Failed to fetch data:", e)
