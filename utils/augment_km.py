import logging
import os
import random

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import cursor as Psycopg2Cursor

logging.basicConfig(level=logging.INFO)

load_dotenv()

rentcar_dbconfig = {
    "dbname": os.getenv("POSTGRES_RENTCAR_DB"),
    "user": os.getenv("POSTGRES_MILEAGE_USER"),
    "password": os.getenv("POSTGRES_RENTCAR_PASSWORD"),
    "host": "localhost",
    "port": 5432,
}

mileage_dbconfig = {
    "dbname": os.getenv("POSTGRES_MILEAGE_DB"),
    "user": os.getenv("POSTGRES_MILEAGE_USER"),
    "password": os.getenv("POSTGRES_MILEAGE_PASSWORD"),
    "host": "localhost",
    "port": 5433,
}


def get_active_car_ids(cursor: Psycopg2Cursor) -> list:
    """
    Fetches the IDs of all active cars.
    args:
        cursor: Psycopg2Cursor - psycopg2 cursor Psycopg2Cursor
    returns:
        list - list of active car IDs
    """
    cursor.execute("SELECT id FROM car WHERE is_available = FALSE")
    return [row[0] for row in cursor.fetchall()]


def insert_mileage_data(cursor: Psycopg2Cursor, car_id: int) -> None:
    """
    Insert
    """
    cursor.execute(
        """
        INSERT INTO daily_mileage (car_id, daily_km)
        VALUES (%s, %s)
    """,
        (car_id, random.randint(0, 300)),
    )


if __name__ == "__main__":
    try:
        with psycopg2.connect(**rentcar_dbconfig) as conn:
            with conn.cursor() as cur:
                active_car_ids = get_active_car_ids(cursor=cur)
        if not active_car_ids:
            logging.warning("No active cars found. Skipping mileage data insertion.")
            exit()

        with psycopg2.connect(**mileage_dbconfig) as conn:
            with conn.cursor() as cur:
                for id_car in active_car_ids:
                    insert_mileage_data(cursor=cur, car_id=id_car)
            conn.commit()
            logging.info("Data generated successfully.")
    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
