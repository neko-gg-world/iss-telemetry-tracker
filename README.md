ISS Real-Time Telemetry Pipeline & Dashboard

A live data ingestion pipeline and interactive analytics dashboard tracking the International Space Station in real time.

Architecture
- **Ingestion:** Consumes live coordinates and velocity via the WhereTheISS REST API.
- **Storage:** Persists raw telemetry records into a local **SQLite** relational schema.
- **Analytics & UI:** Built with **Pandas** and **Streamlit** to provide live KPI metrics, interactive map tracking, and telemetry trends.

##  How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
