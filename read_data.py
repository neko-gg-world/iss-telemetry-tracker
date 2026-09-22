import sqlite3

# 1. Connect to the database file
conn = sqlite3.connect("iss_records.db")
cursor = conn.cursor()

# 2. Write our query: Ask for all rows from the table
cursor.execute("SELECT * FROM telemetry")

# 3. Grab all the results
rows = cursor.fetchall()

# 4. Print each row cleanly
print("ID | Timestamp   | Latitude | Longitude | Altitude (km) | Speed (km/h)")
print("-" * 65)

for row in rows:
    print(f"{row[0]:<2} | {row[1]} | {row[2]:<8.2f} | {row[3]:<9.2f} | {row[4]:<13.1f} | {row[5]:<10.1f}")

# Clean up connection
conn.close()
