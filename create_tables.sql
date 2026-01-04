-- ===========================
-- 1. Customers Table
-- ===========================
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT UNIQUE,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample customers
INSERT OR IGNORE INTO customers (name, phone, email) VALUES
('Alice Zhang', '1234567890', 'alice@example.com'),
('Bob Li', '0987654321', 'bob@example.com');

-- ===========================
-- 2. Doctors Table
-- ===========================
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT,
    phone TEXT,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample doctors
INSERT OR IGNORE INTO doctors (name, specialization, phone, email) VALUES
('Dr. Wang', 'Orthodontics', '1112223333', 'wang@example.com'),
('Dr. Li', 'General Dentistry', '4445556666', 'li@example.com');

-- ===========================
-- 3. Services Table
-- ===========================
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    duration_minutes INTEGER NOT NULL,
    price REAL NOT NULL,
    doctor_id INTEGER,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- Sample services
INSERT OR IGNORE INTO services (name, description, duration_minutes, price, doctor_id) VALUES
('Cleaning', 'Teeth cleaning and polishing', 30, 200.0, 2),
('Extraction', 'Remove damaged tooth', 60, 500.0, 2),
('Checkup', 'Oral health examination', 20, 100.0, 1);

-- ===========================
-- 4. Time Slots Table
-- ===========================
CREATE TABLE IF NOT EXISTS time_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- Sample time slots
INSERT OR IGNORE INTO time_slots (doctor_id, date, time, is_available) VALUES
(1, '2026-01-05', '09:00', 1),
(1, '2026-01-05', '10:00', 1),
(2, '2026-01-05', '09:00', 1),
(2, '2026-01-05', '10:00', 1);

-- ===========================
-- 5. Appointments Table
-- ===========================
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    doctor_id INTEGER,
    date DATE NOT NULL,
    time TIME NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('confirmed', 'pending', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (service_id) REFERENCES services(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- Sample appointment
INSERT OR IGNORE INTO appointments (service_id, customer_id, doctor_id, date, time, status) VALUES
(1, 1, 2, '2026-01-05', '09:00', 'confirmed');
