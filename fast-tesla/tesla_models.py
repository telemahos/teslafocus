import json
import sys
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy setup
engine = create_engine('sqlite:///tesla_inventory.db', echo=True)
Base = declarative_base()

class TeslaModel3(Base):
    __tablename__ = 'tesla_model_3'

    id = Column(Integer, primary_key=True)
    model = Column(String)               # Tesla Model
    available_from = Column(String)      # Available from
    available_to = Column(String)        # Available to
    heat_pump = Column(String)           # Heat pump
    battery_capacity = Column(Float)     # Battery capacity (kWh)
    usable_battery_capacity = Column(Float)  # Usable battery capacity (kWh)
    battery_type = Column(String)        # Battery type
    cathode_material = Column(String)    # Cathode material
    form_factor = Column(String)         # Form factor
    battery_name = Column(String)        # Battery name
    max_charging_power = Column(Float)   # Max charging power (kW)
    charging_time = Column(Float)        # Charging time (min)
    charging_speed = Column(Float)       # Charging speed (km/h)
    acceleration_0_100 = Column(Float)   # Acceleration 0-100 km/h
    top_speed = Column(Integer)          # Top speed
    power = Column(Integer)              # Power (PS)
    max_torque = Column(Integer)         # Max torque (Nm)
    drive = Column(String)               # Drive
    wltp_range = Column(Integer)         # WLTP range (km)

# Tabelle erstellen
Base.metadata.create_all(engine)

# Daten einfügen
model3_data = [
    ['Model 3 ', 'December 2021', 'October 2023', True   , 60.0, 57.5, 'Lithium-Ion', 'LFP', 'Prismatic', 'CATL LFP60', 170, 25, 680, 6.1, 225, 283, 420, 'RWD', 495],
    ['Model 3 Standard Plus LFP', 'January 2022', 'August 2023', True   , 55.0, 52.5, 'Lithium-Ion', 'LFP', 'Prismatic', 'CATL LFP60', 170, 25, 680, 6.1, 225, 283, 420, 'RWD', 495],
    ['Model 3 Standard Plus', 'November 2020', 'December 2021', True, 55.0, 51.0, 'Lithium-Ion', 'LFP', 'Prismatic', 'CATL LFP55', 170, 24, 610, 5.6, 225, 325, 420, 'RWD', 448],
    ['Model 3 Standard Plus', 'February 2021', 'December 2021', True, 55.0, 51.0, 'Lithium-Ion', 'NCA', 'Cylindrical', 'Panasonic 2170L', 170, 21, 700, 5.6, 225, 283, 420, 'RWD', 448],
    ['Model 3 Long Range', 'April 2019', 'October 2020', 'No Data', 51.0, 49.0, 'Lithium-Ion', 'NCA', 'Cylindrical', 'Panasonic 2170C', 170, 21, 640, 5.6, 225, 325, 420, 'RWD', 409],
    ['Model 3 Long Range', 'December 2021', 'August 2023', True, 78.1, 75.0, 'Lithium-Ion', 'NCM', 'Cylindrical', 'LG M50', 250, 27, 750, 4.4, 233, 498, 493, 'AWD', 614],
]

# Daten in die Tabelle einfügen
with engine.begin() as conn:
    for row in model3_data:
        conn.execute(TeslaModel3.__table__.insert(), [
            {'model': row[0], 'available_from': row[1], 'available_to': row[2], 'heat_pump': row[3], 
             'battery_capacity': row[4], 'usable_battery_capacity': row[5], 'battery_type': row[6], 
             'cathode_material': row[7], 'form_factor': row[8], 'battery_name': row[9], 
             'max_charging_power': row[10], 'charging_time': row[11], 'charging_speed': row[12], 
             'acceleration_0_100': row[13], 'top_speed': row[14], 'power': row[15], 
             'max_torque': row[16], 'drive': row[17], 'wltp_range': row[18]}
        ])

class TeslaModelY(Base):
    __tablename__ = 'tesla_model_y'

    id = Column(Integer, primary_key=True)
    model = Column(String)               # Tesla Model
    available_from = Column(String)      # Available from
    available_to = Column(String)        # Available to
    heat_pump = Column(String)           # Heat pump
    battery_capacity = Column(Float)     # Battery capacity (kWh)
    usable_battery_capacity = Column(Float)  # Usable battery capacity (kWh)
    battery_type = Column(String)        # Battery type
    cathode_material = Column(String)    # Cathode material
    form_factor = Column(String)         # Form factor
    battery_name = Column(String)        # Battery name
    max_charging_power = Column(Float)   # Max charging power (kW)
    charging_time = Column(Float)        # Charging time (min)
    charging_speed = Column(Float)       # Charging speed (km/h)
    acceleration_0_100 = Column(Float)   # Acceleration 0-100 km/h
    top_speed = Column(Integer)          # Top speed
    power = Column(Integer)              # Power (PS)

# Tabelle erstellen
Base.metadata.create_all(engine)

# Daten einfügen
modely_data = [
    ['Model Y Standard', 'May 2023', None, True, 60.0, 57.5, 'Lithium-Ion', 'LFP', 'Prismatic', 'BYD BLADE', 175, 18, 810, 6.9, 217, 299],
    ['Model Y Standard', 'November 2022', None, True, 60.0, 57.5, 'Lithium-Ion', 'LFP', 'Prismatic', 'CATL LFP60', 170, 25, 580, 6.9, 217, 299],
    ['Model Y Long Range RWD', 'April 2024', None, True, 78.1, 75.0, 'Lithium-Ion', 'NCM', 'Cylindrical', 'Keine Daten', 250, 27, 710, 5.9, 217, 340],
    ['Model Y Long Range AWD', 'February 2022', 'January 2022', True, 78.1, 75.0, 'Lithium-Ion', 'NCM', 'Cylindrical', 'LG M50', 250, 27, 670, 5.0, 217, 514],
    ['Model Y Long Range AWD', 'August 2021', None, True, 75.0, 72.0, 'Lithium-Ion', 'NCM', 'Cylindrical', 'LG M48', 250, 29, 610, 5.0, 217, 514],
]

# Daten in die Tabelle einfügen
with engine.begin() as conn:
    for row in modely_data:
        conn.execute(TeslaModelY.__table__.insert(), [
            {'model': row[0], 'available_from': row[1], 'available_to': row[2], 'heat_pump': row[3], 
             'battery_capacity': row[4], 'usable_battery_capacity': row[5], 'battery_type': row[6], 
             'cathode_material': row[7], 'form_factor': row[8], 'battery_name': row[9], 
             'max_charging_power': row[10], 'charging_time': row[11], 'charging_speed': row[12], 
             'acceleration_0_100': row[13], 'top_speed': row[14], 'power': row[15]}
        ])


# Create the tables if they don't exist
Base.metadata.create_all(engine)

# Session erstellen
Session = sessionmaker(bind=engine)

# Funktion zum Extrahieren des Datums aus dem Dateinamen
# def extract_date_from_filename(json_filename):
#     date_str = json_filename.split('_')[0]  # Annahme: Das Datum ist der erste Teil des Dateinamens vor dem ersten Unterstrich
#     return datetime.strptime(date_str, "%Y%m%d").date()

#        

        

logger.info("Skript wurde erfolgreich ausgeführt.")