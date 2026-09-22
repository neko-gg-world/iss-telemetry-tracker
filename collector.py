import time
import sqlite3
import requests

API_URL = "https://api.wheretheiss.at/v1/satellites/25544"
DB_NAME = "iss_records.db"

# 1. Connect to SQLite (creates the file automatically if it doesn't exist)
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# 2. Write our first SQL query: Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER,
    latitude REAL,
    longitude REAL,
    altitude REAL,
    velocity REAL
)
""")
conn.commit()
print("Database and table ready.")


def save_current_location():
    # Fetch from API
    response = requests.get(API_URL)
    data = response.json()

    # 3. Write SQL to INSERT data into our table
    cursor.execute("""
        INSERT INTO telemetry (timestamp, latitude, longitude, altitude, velocity)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["latitude"],
        data["longitude"],
        data["altitude"],
        data["velocity"]
    ))

    # Commit tells the database to permanently save the changes
    conn.commit()

    print(f"Logged point: Lat {data['latitude']:.2f}, Lon {data['longitude']:.2f} | Speed: {data['velocity']:.0f} km/h")


# Collect 5 data points spaced 3 seconds apart
print("Starting telemetry collection...")
for i in range(5):
    save_current_location()
    time.sleep(3)

# Close connection cleanly when done
conn.close()
print("Finished! All 5 records saved to iss_records.db.")