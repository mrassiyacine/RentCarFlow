import logging
import os
import random
from datetime import datetime, timedelta

import psycopg2
from dotenv import load_dotenv
from faker import Faker
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

fake = Faker("fr_FR")


def populate_car_models(cursor: Psycopg2Cursor) -> None:
    """
    Populates the 'car_models' table with predefined car models.
    args:
        cursor: Psycopg2Cursor - psycopg2 cursor Psycopg2Cursor
    """
    car_models_data = [
        {
            "model_name": "Tesla Model 3",
            "monthly_rental_rate": 1200.00,
            "km_per_month": 1500,
            "cost_per_km_over_limit": 0.30,
        },
        {
            "model_name": "Toyota Corolla",
            "monthly_rental_rate": 800.00,
            "km_per_month": 1200,
            "cost_per_km_over_limit": 0.25,
        },
        {
            "model_name": "Audi Q5",
            "monthly_rental_rate": 1500.00,
            "km_per_month": 1000,
            "cost_per_km_over_limit": 0.40,
        },
        {
            "model_name": "Mercedes Class E",
            "monthly_rental_rate": 1800.00,
            "km_per_month": 800,
            "cost_per_km_over_limit": 0.50,
        },
    ]

    for model in car_models_data:
        cursor.execute(
            """
            INSERT INTO car_models
                       (model_name,
                       monthly_rental_rate,
                       km_limit_per_month,
                       cost_per_extra_km)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (model_name) DO NOTHING
        """,
            (
                model["model_name"],
                model["monthly_rental_rate"],
                model["km_per_month"],
                model["cost_per_km_over_limit"],
            ),
        )


def populate_customers(cursor: Psycopg2Cursor, num_customers: int) -> None:
    """
    Populates the 'customers' table.
    args:
        cursor: Psycopg2Cursor - psycopg2 cursor Psycopg2Cursor
        num_customers: int - number of customers
    """
    for _ in range(num_customers):
        cursor.execute(
            """
            INSERT INTO customer
                        (full_name, email, phone_number)
            VALUES (%s, %s, %s)
        """,
            (fake.name(), fake.email(), fake.phone_number()),
        )


def populate_cars(cursor: Psycopg2Cursor, nums_cars: int) -> None:
    """
    Populates the 'cars' table.
    args:
        cursor: Psycopg2Cursor - psycopg2 cursor Psycopg2Cursor
        nums_cars: int - number of cars
    """
    cursor.execute("SELECT id FROM car_models")
    models_id = [row[0] for row in cursor.fetchall()]

    for _ in range(nums_cars):
        cursor.execute(
            """
            INSERT INTO car
                        (model_id,license_plate, is_available)
            VALUES (%s, %s, %s)
        """,
            (fake.random_element(models_id), fake.license_plate(), True),
        )


def _get_next_month() -> str:
    """
    Returns the first day of the next month in YYYY-MM-DD format.
    If the current month is December, the next month is January of the next year.
    """
    today = datetime.now()
    next_month = today.replace(day=1) + timedelta(days=32)
    return next_month.replace(day=1).strftime("%Y-%m-%d")


def populate_contracts(cursor: Psycopg2Cursor, num_contracts: int) -> None:
    """
    Populates the 'contract' table with monthly rental contracts.

    Args:
        cursor: psycopg2 cursor Psycopg2Cursor
        num_contracts: int - number of contracts to generate
    """
    cursor.execute("SELECT id FROM customer")
    customer_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM car WHERE is_available = TRUE")
    car_ids = [row[0] for row in cursor.fetchall()]

    if not car_ids:
        logging.error("No available cars found.")
        return

    for _ in range(num_contracts):
        customer_id = random.choice(customer_ids)

        car_id = random.choice(car_ids)

        month = _get_next_month()

        cursor.execute(
            """
            INSERT INTO contract (customer_id, car_id, month_contract, total_km_used)
            VALUES (%s, %s, %s, %s)
        """,
            (customer_id, car_id, month, 0),
        )
        cursor.execute(
            """
                        UPDATE car
                        SET is_available = FALSE
                        WHERE id = %s """,
            (car_id,),
        )
        car_ids.remove(car_id)


if __name__ == "__main__":
    try:
        with psycopg2.connect(**rentcar_dbconfig) as conn:
            with conn.cursor() as cur:
                # populate_car_models(cur)
                # populate_customers(cur, 50)
                # populate_cars(cur, 70)
                populate_contracts(cur, 60)
            conn.commit()

            logging.info("Data generated successfully.")
    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
