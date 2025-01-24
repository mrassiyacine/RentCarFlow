CREATE TABLE IF NOT EXISTS daily_mileage (
    mileage_id SERIAL,
    car_id INTEGER NOT NULL,
    daily_km INTEGER NOT NULL,
    recorded_at DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (car_id, recorded_at)
);
