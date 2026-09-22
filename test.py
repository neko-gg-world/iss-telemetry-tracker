import requests


url = "https://api.wheretheiss.at/v1/satellites/25544"


response = requests.get(url)


data = response.json()


print("Satellite Data Received:")
print(data)

# Extract and display specific fields
print("\n--- Telemetry Readout ---")
print(f"Latitude:  {data['latitude']}")
print(f"Longitude: {data['longitude']}")
print(f"Altitude:  {data['altitude']} km")
print(f"Speed:     {data['velocity']} km/h")