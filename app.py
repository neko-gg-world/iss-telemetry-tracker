import sqlite3
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="ISS Telemetry Analytics", layout="wide")

API_URL = "https://api.wheretheiss.at/v1/satellites/25544"
DB_NAME = "iss_records.db"


def fetch_and_store_telemetry():
    """Extracts live data from API and Loads it into SQLite (ETL step)."""
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Ensure table exists
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

        # Insert new coordinate
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

        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Error fetching live telemetry: {e}")


# 1. Action Controls
col_title, col_btn = st.columns([4, 1])
with col_title:
    st.title("🛰️ ISS Real-Time Orbital Analytics")
    st.caption("Live telemetry ingestion pipeline via REST API, persisted in SQLite.")

with col_btn:
    st.write("")
    if st.button("📡 Log New Location", use_container_width=True):
        fetch_and_store_telemetry()
        st.rerun()

# 2. Query Data from SQLite
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM telemetry ORDER BY id DESC", conn)
conn.close()

if df.empty:
    st.warning("No records found in database yet. Click 'Log New Location' above.")
else:
    # 3. Latest Telemetry KPIs
    latest = df.iloc[0]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Current Latitude", f"{latest['latitude']:.2f}°")
    kpi2.metric("Current Longitude", f"{latest['longitude']:.2f}°")
    kpi3.metric("Altitude", f"{latest['altitude']:.1f} km")
    kpi4.metric("Velocity", f"{latest['velocity']:.0f} km/h")

    st.divider()

    # 4. Trajectory Map
    st.subheader(f"📍 Flight Path ({len(df)} Points Logged)")
    st.map(df[["latitude", "longitude"]])

    st.divider()

    # 5. Database Log Viewer
    st.subheader("🗄️ Raw Telemetry Log (SQLite)")
    st.dataframe(df, use_container_width=True) 

    st.divider()

    # 6. Analytics & Trend Visualizations
    st.subheader("📈 Telemetry Analytics")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.caption("Velocity Over Logged Sequence (km/h)")
        # Sort ascending by id so the line chart moves left-to-right chronologically
        st.line_chart(df.sort_values("id").set_index("id")["velocity"])

    with chart_col2:
        st.caption("Orbital Altitude Over Logged Sequence (km)")
        st.line_chart(df.sort_values("id").set_index("id")["altitude"])