from app.mileage import router as mileage_router
from fastapi import FastAPI

app = FastAPI(title="Daily Mileage API", version="1.0")
app.include_router(mileage_router)


@app.get("/")
def root():
    """returns a welcome message"""
    return {"message": "Welcome to the Mileage API"}
