import logging
import os
from datetime import datetime

import psycopg2
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()


rentcar_dbconfig = {
    "dbname": os.getenv("POSTGRES_RENTCAR_DB"),
    "user": os.getenv("POSTGRES_MILEAGE_USER"),
    "password": os.getenv("POSTGRES_RENTCAR_PASSWORD"),
    "host": "localhost",
    "port": 5432,
}


def get_daily_mileage(api_endpoint: str, date: str) -> dict:
    """
    Fetches the daily mileage records for today.
    args:
        endpoint: str - API endpoint
        date: str - date to fetch mileage records for
    returns:
        dict - daily mileage records
    """
    query = f"{api_endpoint}/mileage/date/{date}"
    response = requests.get(query, timeout=15)
    if response.status_code != 200:
        response.raise_for_status()
    return response.json()


def update_mileage_contract(mileage_data: dict) -> None:
    """
    Updates the mileage records in the daily_mileage table.
    args:
        data: dict - mileage records
    """
    logging.info("Updating mileage records in the contract table.")
    with psycopg2.connect(**rentcar_dbconfig) as conn:
        with conn.cursor() as cur:
            for record in mileage_data:
                car_id = record["car_id"]
                daily_km = record["daily_km"]
                query = """UPDATE contract
                           SET total_km_used = total_km_used + %s
                           WHERE car_id = %s"""
                cur.execute(query, (daily_km, car_id))
                logging.info(f"Updated mileage for car_id: {car_id}")
        conn.commit()


if __name__ == "__main__":
    ENDPOINT = "http://0.0.0.0:8000"
    data = get_daily_mileage(
        api_endpoint=ENDPOINT, date=datetime.now().strftime("%Y-%m-%d")
    )
    update_mileage_contract(data)
