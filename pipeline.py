from dagster import op, job
import subprocess


@op
def scrape_telegram_data():
    print("Running Telegram scraper...")
    subprocess.run(["python", "src/scraper.py"], check=True)


@op
def load_raw_to_postgres():
    print("Loading raw data into PostgreSQL...")
    subprocess.run(["python", "src/load_to_postgres.py"], check=True)


@op
def run_dbt_transformations():
    print("Running dbt transformations...")
    subprocess.run(["dbt", "run"], cwd="medical_warehouse", check=True)


@op
def run_yolo_enrichment():
    print("Running YOLO object detection...")
    subprocess.run(["python", "src/yolo_detect.py"], check=True)

    print("Loading YOLO detections into PostgreSQL...")
    subprocess.run(["python", "scripts/load_yolo_to_postgres.py"], check=True)


@job
def medical_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
