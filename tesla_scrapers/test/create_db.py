import sqlite3

# Verbindung zur SQLite-Datenbank herstellen (erstellt die Datei, falls nicht vorhanden)
conn = sqlite3.connect('vehicles.db')

# Cursor-Objekt erstellen
cursor = conn.cursor()

# Tabelle Vehicles erstellen
cursor.execute('''
CREATE TABLE vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vin TEXT UNIQUE,
    model TEXT,
    year INTEGER,
    entry_date TEXT,
    odometer INTEGER,
    odometer_type TEXT,
    paint TEXT,
    factory_gated_date TEXT,
    first_registration_date TEXT,
    inventory_price REAL,
    is_tax_incentive_eligible BOOLEAN,
    price_after_tax_incentive REAL,
    trim_code TEXT,
    efficiency_class TEXT,
    energy_consumption REAL,
    mass INTEGER,
    power INTEGER,
    in_transit BOOLEAN,
    HasDamagePhotos BOOLEAN,
    damage_disclosure BOOLEAN,
    damage_disclosure_status TEXT,
    actual_vessel_arrival_date TEXT,
    expected_vessel_arrival_date TEXT,
    cpo_refurbishment_status TEXT,
    destination_handling_fee REAL,
    is_at_location BOOLEAN,
    is_charging_connector_included BOOLEAN,
    is_demo BOOLEAN,
    discount REAL,
    language TEXT,
    listing_type TEXT,
    metro_name TEXT,
    original_delivery_date TEXT,
    range TEXT,
    exterior_color TEXT,
    interior_color TEXT,
    drive_unit TEXT,
    top_speed INTEGER,
    acceleration REAL,
    available_status BOOLEAN,
    cpo_warranty TEXT,
    service_contract TEXT,
    city TEXT,
    state TEXT,
    country_code TEXT
)
''')

# Tabelle Pricing erstellen
cursor.execute('''
CREATE TABLE pricing (
    pricing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    date TEXT,
    price REAL,
    currency TEXT,
    FOREIGN KEY(vehicle_id) REFERENCES vehicles(vehicle_id)
)
''')

# Tabelle Features erstellen
cursor.execute('''
CREATE TABLE features (
    feature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    enhance_autopilot TEXT,
    seat_options TEXT,
    sound_system TEXT,
    FOREIGN KEY(vehicle_id) REFERENCES vehicles(vehicle_id)
)
''')

cursor.execute('''
CREATE TABLE images (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    image_url TEXT,
    FOREIGN KEY(vehicle_id) REFERENCES Vehicles(vehicle_id)
)
''')

# Änderungen speichern und die Verbindung schließen
conn.commit()
conn.close()

print("Database created successfully.")
