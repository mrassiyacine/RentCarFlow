CREATE TABLE IF NOT EXISTS car_models (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL UNIQUE,
    monthly_rental_rate DECIMAL(10, 2) NOT NULL,
    km_limit_per_month INT NOT NULL,
    cost_per_extra_km DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS car (
    id SERIAL PRIMARY KEY,
    model_id INT NOT NULL,
    license_plate VARCHAR(15) UNIQUE,
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (model_id) REFERENCES car_models(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS customer (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS contract (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    car_id INT NOT NULL UNIQUE,
    month_contract DATE NOT NULL,
    total_km_used INT DEFAULT 0,
    creared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE,
    FOREIGN KEY (car_id) REFERENCES car(id) ON DELETE CASCADE
);