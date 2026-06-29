import pandas as pd
from sqlalchemy import create_engine

# ------------------------
# CONFIG
# ------------------------
CSV_PATH = "data/processed/yolo_detections.csv"

DB_URL = "postgresql://postgres:postgres@localhost:5432/medical_warehouse"

# ------------------------
# LOAD DATA
# ------------------------
df = pd.read_csv(CSV_PATH)

# Create DB connection
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://new@localhost:5432/medical_warehouse"
)

# Write to table
df.to_sql(
    "yolo_detections",
    engine,
    if_exists="replace",
    index=False
)

print("YOLO data loaded into PostgreSQL successfully.")
