from datetime import date

from pydantic import BaseModel


class DailyMileageResponse(BaseModel):
    """
    DailyMileageResponse class for Pydantic.
    """

    car_id: int
    daily_km: int
    recorded_at: date
