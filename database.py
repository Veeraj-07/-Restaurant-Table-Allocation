import sqlite3

# Connect to database
conn = sqlite3.connect("restaurant.db")

cursor = conn.cursor()


# ==========================================
# CREATE USERS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")


# ==========================================
# CREATE RESTAURANT TABLES
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS restaurant_tables (
    table_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_number INTEGER UNIQUE NOT NULL,
    capacity INTEGER NOT NULL,
    status TEXT DEFAULT 'Available'
)
""")


# ==========================================
# CREATE RESERVATIONS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    table_id INTEGER,
    booking_date TEXT NOT NULL,
    booking_time TEXT NOT NULL,
    guests INTEGER NOT NULL,
    status TEXT DEFAULT 'Reserved',

    FOREIGN KEY (table_id)
    REFERENCES restaurant_tables(table_id)
)
""")


# ==========================================
# INSERT DEFAULT ADMIN ACCOUNT
# ==========================================

cursor.execute("""
INSERT OR IGNORE INTO users
(name, email, password, role)
VALUES (?, ?, ?, ?)
""", (
    "Admin",
    "admin@restaurant.com",
    "admin123",
    "admin"
))


# ==========================================
# INSERT RESTAURANT TABLES
# ==========================================

tables = [
    (1, 2, "Available"),
    (2, 2, "Available"),
    (3, 4, "Available"),
    (4, 4, "Available"),
    (5, 6, "Available"),
    (6, 6, "Available")
]

cursor.executemany("""
INSERT OR IGNORE INTO restaurant_tables
(table_number, capacity, status)
VALUES (?, ?, ?)
""", tables)


# ==========================================
# SAVE CHANGES
# ==========================================

conn.commit()

conn.close()

print("Database and tables created successfully!")
print("Admin account created successfully!")
print("Email: admin@restaurant.com")
print("Password: admin123")