from datetime import date
from typing import List

from app.db import DailyMileage, get_db_connection
from app.schemas import DailyMileageResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/mileage/", response_model=List[DailyMileageResponse])
def get_all_mileage(db: Session = Depends(get_db_connection)):
    """
    Returns all mileage records.
    """
    records = db.query(DailyMileage).all()
    print(records)
    if not records:
        raise HTTPException(status_code=404, detail="No mileage records found")
    return records


@router.get("/mileage/{car_id}", response_model=list[DailyMileageResponse])
def get_mileage_by_car(car_id: int, db: Session = Depends(get_db_connection)):
    """
    Returns all mileage records for a specific car.
    """
    mileage_records = db.query(DailyMileage).filter(DailyMileage.car_id == car_id).all()
    if not mileage_records:
        raise HTTPException(
            status_code=404, detail=f"No mileage records found for car_id {car_id}"
        )
    return mileage_records


@router.get("/mileage/{car_id}/{recorded_at}", response_model=DailyMileageResponse)
def get_mileage_by_car_and_date(
    car_id: int, recorded_at: date, db: Session = Depends(get_db_connection)
):
    """
    Returns a specific mileage record for a specific car and date.
    """
    mileage_record = (
        db.query(DailyMileage)
        .filter(DailyMileage.car_id == car_id, DailyMileage.recorded_at == recorded_at)
        .first()
    )
    if not mileage_record:
        raise HTTPException(
            status_code=404,
            detail=f"No mileage record found for car_id {car_id} on {recorded_at}",
        )
    return mileage_record
