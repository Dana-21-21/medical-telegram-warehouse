# Medical Telegram Data Warehouse

## Project Overview

This project implements a modern ELT data pipeline for Ethiopian medical Telegram channels. The objective is to collect Telegram messages, store them in a structured data lake, and transform the raw data into an analytics-ready star schema using dbt and PostgreSQL.

The warehouse enables downstream analytics such as product popularity analysis, channel performance monitoring, medical content trends, and business intelligence dashboards.

---

# Project Architecture

```
Telegram Channels
        │
        ▼
Telegram Scraper (Telethon)
        │
        ▼
JSON Files + Images
        │
        ▼
Raw Data Lake
        │
        ▼
PostgreSQL
(raw.telegram_messages)
        │
        ▼
dbt Transformations
        │
        ▼
Star Schema
 ├── dim_channels
 ├── dim_dates
 └── fct_messages
```

---

# Project Structure

```
medical-telegram-warehouse/

│
├── data/
│   ├── raw/
│   │   ├── telegram_messages.json
│   │   └── images/
│   └── processed/
│
├── medical_warehouse/
│   ├── analyses/
│   ├── macros/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   ├── snapshots/
│   ├── seeds/
│   ├── tests/
│   ├── dbt_project.yml
│   └── README.md
│
├── src/
├── scripts/
├── notebooks/
├── scraper.py
├── requirements.txt
└── README.md
```

---

# Technologies Used

* Python
* Telethon
* PostgreSQL
* dbt
* SQL
* Git
* GitHub

---

# Data Lake Structure

The project follows a layered data architecture.

### Raw Layer

Contains the original Telegram data collected from multiple channels.

Contents include:

* JSON files
* Downloaded images
* Original metadata
* No transformations applied

---

### Staging Layer

The staging layer performs data cleaning and standardization.

Transformations include:

* Timestamp conversion
* Null handling
* Text availability flag
* View count cleaning
* Forward count cleaning
* Message length calculation

---

### Mart Layer

The mart layer contains analytics-ready tables organized using a star schema.

Models include:

* dim_channels
* dim_dates
* fct_messages

---

# Data Quality Tests

Implemented tests include:

## Generic Tests

* Unique channel keys
* Unique dates
* Non-null primary keys
* Relationship integrity
* Foreign key validation

## Custom Tests

* No future message dates
* Positive view counts

All tests passed successfully.

---

# Star Schema

Fact Table

* fct_messages

Dimension Tables

* dim_channels
* dim_dates

The star schema enables efficient analytical queries while minimizing redundancy.

---

# How to Run

Activate the environment

```
source venv/bin/activate
```

Run dbt models

```
dbt run
```

Execute tests

```
dbt test
```

Generate documentation

```
dbt docs generate
```

Serve documentation

```
dbt docs serve
```

Open

```
http://localhost:8080
```

---

# Results

The project successfully:

* Scraped Telegram medical channels
* Built a raw data lake
* Loaded data into PostgreSQL
* Developed dbt staging models
* Created a star schema
* Implemented automated data quality testing
* Generated interactive dbt documentation

---

# Future Work

Future improvements include:

* OCR extraction from medicine images
* Product entity extraction using NLP
* Dashboard development with Power BI or Dash
* Automated scheduling using Airflow
* Incremental dbt models
* Data lineage monitoring

