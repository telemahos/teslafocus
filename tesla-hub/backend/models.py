from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, Date, Float, DateTime 
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, date



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String)
    user_role = Column(Integer) # admin=?, Dev=1, QA=2, BA=3, PM=4, TM=5

#---------------------------------------
class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True, index=True)
    case_nr = Column(String, index = True)
    start_date = Column(Date, index=True)
    due_date = Column(Date, index=True)
    title = Column(String, index = True)
    description = Column(String) 
    tags = Column(String)
    status = Column(Integer, default=0)
    priority = Column(Integer) # Low=1, Medium=2, High=3, Critical=4
    case_type = Column(Integer) # Issue=1, Bug=2, Note=3
    project_id = Column(Integer)
    owner_id = Column(Integer)

#---------------------------------------
class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    project_nr = Column(String)
    start_date = Column(Date)
    due_date = Column(Date)
    title = Column(String, index = True)
    description = Column(String) 
    tags = Column(String)
    active = Column(Boolean, default=False)
    status = Column(Integer, default=0)
    priority = Column(Integer) # Low=0, Medium=1, High=2, Critical=3
    owner_id = Column(Integer)

    
#---------------------------------------
class TeamMember(Base):
    __tablename__ = 'team_members'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer)
    user_id = Column(Integer)
    team_role = Column(Integer)
    assign_date = Column(Date)
    active = Column(Boolean, default=False)
    note = Column(String)

#---------------------------------------
# Define the Car model
class Cars(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True)
    model = Column(String)
    trim = Column(String)
    trim_name = Column(String)
    year = Column(Integer)
    odometer = Column(Integer)
    odometer_type = Column(String)
    color = Column(String)
    interior = Column(String)
    first_registration_date = Column(DateTime)
    damage_disclosure = Column(Float)
    factory_code = Column(String)
    wltp_range = Column (String)
    battery_capacity = Column(Float)
    cabin_config = Column(String)
    country_code = Column(String)
    city = Column(String)
    active = Column(Boolean, default=True)
    OptionCodeList = Column(String)
    first_entry_date = Column(DateTime)
    last_updated = Column(DateTime)
    currency_code = Column(String)
    damage_disclosure_status = Column(String)
    factory_gated_date = Column(DateTime)
    has_damage_photos = Column(Boolean)
    vehicle_history = Column(String)
    warranty_battery_exp_date = Column(DateTime)
    warranty_battery_is_expired = Column(Boolean)
    warranty_battery_mile = Column(Integer)
    warranty_battery_year = Column(Integer)
    warranty_drive_unit_exp_date = Column(DateTime)
    warranty_drive_unit_mile = Column(Integer)
    warranty_drive_unit_year = Column(Integer)
    warranty_mile = Column(Integer)
    warranty_vehicle_exp_date = Column(DateTime)
    warranty_vehicle_is_expired = Column(Boolean)
    warranty_year = Column(Integer)
    used_vehicle_limited_warranty_mile = Column(Integer)
    used_vehicle_limited_warranty_year = Column(Integer)
    odometer_type_short = Column(String)
    photos_count = Column(Integer, default=0)

    prices = relationship("Prices", back_populates="car")


class Prices(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    price = Column(Float)
    date = Column(DateTime)

    car = relationship("Cars", back_populates="prices")

# Definiere das Datenbankmodell für die IDs
class IdModel(Base):
    __tablename__ = "ids"
    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)