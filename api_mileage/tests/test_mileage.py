import unittest
from datetime import date

from app.db import Base, DailyMileage, get_db_connection
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

client = TestClient(app)

DATABASE_URL = "sqlite:///./test.db"
testingEngine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=testingEngine
)


def override_get_db_connection():
    """
    Override the get_db_connection dependency to use the TestingSessionLocal.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db_connection] = override_get_db_connection


class TestMileageAPI(unittest.TestCase):
    """
    Test the Mileage API.
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup the database.
        """
        Base.metadata.create_all(bind=testingEngine)
        db = TestingSessionLocal()
        test_data = [
            DailyMileage(
                mileage_id=1, car_id=1, daily_km=100, recorded_at=date(2025, 1, 1)
            ),
            DailyMileage(
                mileage_id=2, car_id=2, daily_km=100, recorded_at=date(2025, 1, 1)
            ),
            DailyMileage(
                mileage_id=3, car_id=2, daily_km=150, recorded_at=date(2025, 1, 2)
            ),
            DailyMileage(
                mileage_id=4, car_id=3, daily_km=200, recorded_at=date(2025, 1, 3)
            ),
        ]
        db.add_all(test_data)
        db.commit()
        db.close()

    @classmethod
    def tearDownClass(cls):
        """
        Teardown the database.
        """
        Base.metadata.drop_all(bind=testingEngine)

    def test_get_all_mileage(self):
        """Test get all mileage records"""
        response = client.get("/mileage/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 4)

    def test_get_mileage_by_car(self):
        """Test get mileage records by car"""
        response = client.get("/mileage/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["car_id"], 1)

    def test_get_mileage_by_date(self):
        """Test get mileage records by date"""
        response = client.get("/mileage/date/2025-01-01")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["recorded_at"], "2025-01-01")

    def test_get_mileage_by_car_and_date(self):
        """Test get mileage records by car and date"""
        response = client.get("/mileage/1/2025-01-01")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["car_id"], 1)
        self.assertEqual(data["recorded_at"], "2025-01-01")
        self.assertEqual(data["daily_km"], 100)
