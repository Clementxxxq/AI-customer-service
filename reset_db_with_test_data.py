"""
Reset database and insert test data
- 4 doctors
- 20 customers
- 3 services
- 20 booked appointments
"""
import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = "db/clinic.db"

def reset_and_populate_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🗑️  Clearing database...")
    # Drop all tables
    cursor.execute("DROP TABLE IF EXISTS appointments")
    cursor.execute("DROP TABLE IF EXISTS time_slots")
    cursor.execute("DROP TABLE IF EXISTS services")
    cursor.execute("DROP TABLE IF EXISTS doctors")
    cursor.execute("DROP TABLE IF EXISTS customers")
    
    print("📋 Creating table structures...")
    # Create tables
    cursor.executescript("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT UNIQUE,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        phone TEXT,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        duration_minutes INTEGER NOT NULL,
        price REAL NOT NULL,
        doctor_id INTEGER,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    );
    
    CREATE TABLE time_slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        date DATE NOT NULL,
        time TIME NOT NULL,
        is_available BOOLEAN NOT NULL DEFAULT 1,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    );
    
    CREATE TABLE appointments (
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
    """)
    
    print("👨‍⚕️  Adding 4 doctors...")
    doctors = [
        ("Dr. Wang", "Orthodontics", "1112223333", "wang@clinic.com"),
        ("Dr. Chen", "General Dentistry", "2223334444", "chen@clinic.com"),
        ("Dr. Li", "Pediatric Dentistry", "3334445555", "li@clinic.com"),
        ("Dr. Zhang", "Prosthodontics", "4445556666", "zhang@clinic.com"),
    ]
    
    cursor.executemany(
        "INSERT INTO doctors (name, specialization, phone, email) VALUES (?, ?, ?, ?)",
        doctors
    )
    print(f"   ✅ Added {len(doctors)} doctors")
    
    print("🦷 Adding 3 services...")
    services = [
        ("Checkup", "Oral health examination", 20, 100.0),
        ("Cleaning", "Teeth cleaning and polishing", 30, 200.0),
        ("Extraction", "Remove damaged tooth", 60, 500.0),
    ]
    
    cursor.executemany(
        "INSERT INTO services (name, description, duration_minutes, price) VALUES (?, ?, ?, ?)",
        services
    )
    print(f"   ✅ Added {len(services)} services")
    
    print("👥 Adding 20 customers...")
    customer_names = [
        "Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson", "Emma Brown",
        "Frank Miller", "Grace Lee", "Henry Taylor", "Iris Anderson", "Jack Thomas",
        "Karen Jackson", "Leo White", "Mia Harris", "Noah Martin", "Olivia Moore",
        "Peter Clark", "Quinn Lewis", "Ryan Walker", "Sara Hall", "Tom Young"
    ]
    
    customers = []
    for i, name in enumerate(customer_names, 1):
        phone = f"555{10000 + i:05d}"  # 555xxxxx
        email = f"{name.lower().replace(' ', '.')}@example.com"
        customers.append((name, phone, email))
    
    cursor.executemany(
        "INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)",
        customers
    )
    print(f"   ✅ Added {len(customers)} customers")
    
    print("📅 Adding 20 booked appointments...")
    # Generate 20 appointments
    base_date = datetime.now()
    appointments = []
    
    for i in range(1, 21):
        customer_id = i  # Customers 1-20
        doctor_id = (i % 4) + 1  # Doctors 1-4 rotate
        service_id = ((i - 1) % 3) + 1  # Services 1-3 rotate
        
        # Appointment date: today to next 14 days
        days_offset = (i - 1) // 3  # Every 3 appointments, increment a day
        appt_date = (base_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        
        # Appointment time: 9:00, 10:00, 11:00, 14:00, 15:00...
        times = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
        appt_time = times[(i - 1) % len(times)]
        
        # Status: mostly confirmed, some pending
        status = "confirmed" if i % 5 != 0 else "pending"
        
        appointments.append((
            service_id,      # service_id
            customer_id,     # customer_id
            doctor_id,       # doctor_id
            appt_date,       # date
            appt_time,       # time
            status           # status
        ))
    
    cursor.executemany(
        """INSERT INTO appointments 
           (service_id, customer_id, doctor_id, date, time, status) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        appointments
    )
    print(f"   ✅ Added {len(appointments)} appointments")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Database reset completed!")
    print("=" * 60)
    
    # Display statistics
    display_statistics()


def display_statistics():
    """Display database statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n📊 Database Statistics:")
    print("-" * 60)
    
    # Doctors list
    cursor.execute("SELECT id, name FROM doctors")
    doctors = cursor.fetchall()
    print(f"\n👨‍⚕️  Doctors ({len(doctors)}):")
    for doc_id, name in doctors:
        print(f"   {doc_id}. {name}")
    
    # Services list
    cursor.execute("SELECT id, name FROM services")
    services = cursor.fetchall()
    print(f"\n🦷 Services ({len(services)}):")
    for svc_id, name in services:
        print(f"   {svc_id}. {name}")
    
    # Total customers
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]
    print(f"\n👥 Total Customers: {customer_count}")
    
    # Appointments statistics
    cursor.execute("SELECT COUNT(*) FROM appointments")
    appt_count = cursor.fetchone()[0]
    print(f"\n📅 Total Appointments: {appt_count}")
    
    # By status
    cursor.execute("""
        SELECT status, COUNT(*) as count 
        FROM appointments 
        GROUP BY status
    """)
    statuses = cursor.fetchall()
    print("   By Status:")
    for status, count in statuses:
        print(f"      - {status}: {count}")
    
    # By doctor
    cursor.execute("""
        SELECT d.name, COUNT(a.id) as count 
        FROM doctors d
        LEFT JOIN appointments a ON d.id = a.doctor_id
        GROUP BY d.id
    """)
    doc_appts = cursor.fetchall()
    print("   By Doctor:")
    for doc_name, count in doc_appts:
        print(f"      - {doc_name}: {count} appointments")
    
    # By service
    cursor.execute("""
        SELECT s.name, COUNT(a.id) as count 
        FROM services s
        LEFT JOIN appointments a ON s.id = a.service_id
        GROUP BY s.id
    """)
    svc_appts = cursor.fetchall()
    print("   By Service:")
    for svc_name, count in svc_appts:
        print(f"      - {svc_name}: {count} appointments")
    
    print("\n" + "=" * 60)
    
    conn.close()


if __name__ == "__main__":
    try:
        reset_and_populate_db()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
