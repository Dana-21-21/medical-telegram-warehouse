import os
import json
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


# ----------------------------
# PostgreSQL Connection
# ----------------------------

DB_USER = "new"
DB_PASSWORD = ""      # Put your password here if you have one
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "medical_warehouse"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# ----------------------------
# Locate JSON files
# ----------------------------

DATA_PATH = Path("data/raw/telegram_messages")

json_files = list(DATA_PATH.rglob("*.json"))

print(f"\nFound {len(json_files)} JSON files.\n")

# ----------------------------
# Read every JSON
# ----------------------------

all_messages = []

for file in json_files:

    print(f"Reading {file.name}")

    with open(file, "r", encoding="utf-8") as f:

        data = json.load(f)

        if isinstance(data, list):

            all_messages.extend(data)

        else:

            all_messages.append(data)

print(f"\nTotal messages: {len(all_messages)}")

# ----------------------------
# Convert to DataFrame
# ----------------------------

df = pd.json_normalize(all_messages)

print(df.head())

# ----------------------------
# Save into PostgreSQL
# ----------------------------

df.to_sql(

    "telegram_messages",

    engine,

    schema="raw",

    if_exists="replace",

    index=False

)

print("\nData successfully loaded into PostgreSQL.")
