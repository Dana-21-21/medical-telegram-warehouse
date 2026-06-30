from dagster import (
    op,
    job,
    ScheduleDefinition,
    Definitions,
    get_dagster_logger,
)
import subprocess


@op
def scrape_telegram_data():
    logger = get_dagster_logger()
    logger.info("Starting Telegram scraper...")

    try:
        subprocess.run(["python", "src/scraper.py"], check=True)
        logger.info("Telegram scraping completed successfully.")
    except Exception as e:
        logger.error(f"Telegram scraping failed: {e}")
        raise


@op
def load_raw_to_postgres():
    logger = get_dagster_logger()
    logger.info("Loading raw data into PostgreSQL...")

    try:
        subprocess.run(["python", "src/load_to_postgres.py"], check=True)
        logger.info("Raw data loaded successfully.")
    except Exception as e:
        logger.error(f"Loading raw data failed: {e}")
        raise


@op
def run_dbt_transformations():
    logger = get_dagster_logger()
    logger.info("Running dbt transformations...")

    try:
        subprocess.run(["dbt", "run"], cwd="medical_warehouse", check=True)
        logger.info("dbt completed successfully.")
    except Exception as e:
        logger.error(f"dbt failed: {e}")
        raise


@op
def run_yolo_enrichment():
    logger = get_dagster_logger()
    logger.info("Running YOLO detection...")

    try:
        subprocess.run(["python", "src/yolo_detect.py"], check=True)
        subprocess.run(
            ["python", "scripts/load_yolo_to_postgres.py"],
            check=True,
        )

        logger.info("YOLO enrichment completed successfully.")

    except Exception as e:
        logger.error(f"YOLO enrichment failed: {e}")
        raise


@job
def medical_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()


daily_schedule = ScheduleDefinition(
    job=medical_pipeline,
    cron_schedule="0 0 * * *",
    name="daily_medical_pipeline",
)

defs = Definitions(
    jobs=[medical_pipeline],
    schedules=[daily_schedule],
)
