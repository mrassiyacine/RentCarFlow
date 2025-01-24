import logging
import os

from dotenv import load_dotenv
from sqlalchemy import Date, Integer, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

load_dotenv()

logging.basicConfig(level=logging.INFO)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM."""

    pass


class DailyMileage(Base):
    """
    DailyMileage class for SQLAlchemy ORM.
    """

    __tablename__ = "daily_mileage"

    mileage_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    daily_km: Mapped[int] = mapped_column(Integer, nullable=False)
    recorded_at: Mapped[str] = mapped_column(
        Date, server_default=func.current_date(), primary_key=True
    )


DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv('POSTGRES_MILEAGE_USER')}:{os.getenv('POSTGRES_MILEAGE_PASSWORD')}"
    f"@{os.getenv('POSTGRES_MILEAGE_HOST')}:{os.getenv('POSTGRES_MILEAGE_PORT')}"
    f"/{os.getenv('POSTGRES_MILEAGE_DB')}"
)
try:
    logging.info("Attempting to connect to the database...")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    logging.info("Database connection established successfully.")
except Exception as e:
    logging.error(f"Error connecting to the database: {e}")
    raise


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_connection():
    """
    Opens a database connection.
    """
    db = None
    try:
        logging.info("Opening a new database session...")
        db = SessionLocal()
        yield db
    except Exception as e:
        logging.error(f"Database session error: {e}")
        raise
    finally:
        if db is not None:
            db.close()
            logging.info("Database session closed.")
