import json
import sys
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from battery_utils import calculate_battery_capacity

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy setup
engine = create_engine('sqlite:///tesla_inventory.db', echo=True)

# engine = create_engine('postgresql://postgres:changethis@localhost:5432/app', echo=True)

Base = declarative_base()


# Define the Car model
class Cars(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
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

    prices = relationship("Prices", back_populates="cars")
    photos = relationship("Photos", back_populates="cars")

# Define the Price model
class Prices(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    price = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)

    cars = relationship("Cars", back_populates="prices")

# Define the Photo model
class Photos(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    image_url = Column(String)

    cars = relationship("Cars", back_populates="photos")


# Define the ModelStats model with a timestamp column
class ModelStats(Base):
    __tablename__ = 'model_stats'
    id = Column(Integer, primary_key=True)
    model = Column(String)  #,unique=True
    min_price = Column(Float)
    max_price = Column(Float)
    avg_price = Column(Float)
    count = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Create the tables if they don't exist
Base.metadata.create_all(engine)

# Session erstellen
Session = sessionmaker(bind=engine)


def process_model_stats(session, model_data, timestamp):
    # Extract the model price stats from the provided JSON data
    model_price_stats = model_data.get('model_price_stats', {})

    for model, stats in model_price_stats.items():
        # Extract stats for each model
        min_price = stats.get('min')
        max_price = stats.get('max')
        avg_price = stats.get('avg')
        count = stats.get('count')

        # Round avg_price to the nearest thousand
        avg_price_rounded = round(avg_price, -3)

        # Create a new record instead of updating the existing one
        model_stat = ModelStats(
            model=model,
            min_price=min_price,
            max_price=max_price,
            avg_price=avg_price_rounded,
            count=count,
            timestamp=timestamp  # Use the extracted timestamp
        )
        session.add(model_stat)

    session.commit()


#        
def process_json_file(json_filename):
    try:
        # Überprüfen Sie, ob der Dateiname einen Zeitstempel enthält
        if '_' not in json_filename:
            raise ValueError("Der Dateiname muss einen Zeitstempel enthalten.")
            
        timestamp_str = json_filename.split('_')[2] + '_' + json_filename.split('_')[3].split('.')[0]
        timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')

        # JSON-Datei öffnen und laden
        with open(json_filename, 'r') as file:
            data = json.load(file)
        
        with Session() as session:
            vehicles = data.get('results', [])
            processed_vins = set()

            for vehicle in vehicles:
                if not isinstance(vehicle, dict):
                    logger.warning(f"Skipping invalid vehicle data: {vehicle}")
                    continue
                
                vin = vehicle.get('VIN')
                if vin in processed_vins:
                    logger.warning(f"Vin {vin} wurde bereits verarbeitet. Skipping.")
                    continue
                processed_vins.add(vin)

                # Process constant data
                car = session.query(Cars).filter_by(vin=vin).first()
                if not car:
                    wltp_range = get_wltp_range(vehicle)
                    model = vehicle.get('Model')
                    trim = ','.join(vehicle.get('TRIM', [])) if isinstance(vehicle.get('TRIM'), list) else ''
                    
                    battery_capacity = calculate_battery_capacity(model, trim, wltp_range)
                    
                    car = Cars(
                        vin=vehicle.get('VIN'),
                        model=vehicle.get('Model'),
                        trim=','.join(vehicle.get('TRIM', [])) if isinstance(vehicle.get('TRIM'), list) else '',
                        trim_name=vehicle.get('TrimName'),
                        year=int(vehicle.get('Year', 0)),
                        odometer=vehicle.get('Odometer', 0),
                        odometer_type=vehicle.get('OdometerType'),
                        color=vehicle.get('PAINT', [''])[0] if isinstance(vehicle.get('PAINT'), list) else '',
                        interior=vehicle.get('INTERIOR', [''])[0] if isinstance(vehicle.get('INTERIOR'), list) else '',
                        damage_disclosure=vehicle.get('DamageDisclosure', False),
                        factory_code=vehicle.get('FactoryCode'),
                        wltp_range=get_wltp_range(vehicle),
                        battery_capacity=battery_capacity,
                        cabin_config=','.join(vehicle.get('CABIN_CONFIG', [])) if isinstance(vehicle.get('CABIN_CONFIG'), list) else '',
                        country_code=vehicle.get('CountryCode'),
                        city=vehicle.get('City'),
                        first_registration_date=datetime.strptime(vehicle.get('FirstRegistrationDate', ''), '%Y-%m-%dT%H:%M:%S') if vehicle.get('FirstRegistrationDate') else None,
                        currency_code=vehicle.get('CurrencyCode'),
                        damage_disclosure_status=vehicle.get('DamageDisclosureStatus'),
                        factory_gated_date=datetime.strptime(vehicle.get('FactoryGatedDate', ''), '%Y-%m-%dT%H:%M:%S.%f') if vehicle.get('FactoryGatedDate') else None,
                        has_damage_photos=vehicle.get('HasDamagePhotos', False),
                        vehicle_history=vehicle.get('VehicleHistory'),
                        warranty_battery_exp_date=datetime.strptime(vehicle.get('WarrantyBatteryExpDate', ''), '%Y-%m-%dT%H:%M:%SZ') if vehicle.get('WarrantyBatteryExpDate') else None,
                        warranty_battery_is_expired=vehicle.get('WarrantyBatteryIsExpired', False),
                        warranty_battery_mile=vehicle.get('WarrantyBatteryMile'),
                        warranty_battery_year=vehicle.get('WarrantyBatteryYear'),
                        warranty_drive_unit_exp_date=datetime.strptime(vehicle.get('WarrantyDriveUnitExpDate', ''), '%Y-%m-%dT%H:%M:%SZ') if vehicle.get('WarrantyDriveUnitExpDate') else None,
                        warranty_drive_unit_mile=vehicle.get('WarrantyDriveUnitMile'),
                        warranty_drive_unit_year=vehicle.get('WarrantyDriveUnitYear'),
                        warranty_mile=vehicle.get('WarrantyMile'),
                        warranty_vehicle_exp_date=datetime.strptime(vehicle.get('WarrantyVehicleExpDate', ''), '%Y-%m-%dT%H:%M:%SZ') if vehicle.get('WarrantyVehicleExpDate') else None,
                        warranty_vehicle_is_expired=vehicle.get('WarrantyVehicleIsExpired', False),
                        warranty_year=vehicle.get('WarrantyYear'),
                        used_vehicle_limited_warranty_mile=vehicle.get('UsedVehicleLimitedWarrantyMile'),
                        used_vehicle_limited_warranty_year=vehicle.get('UsedVehicleLimitedWarrantyYear'),
                        odometer_type_short=vehicle.get('OdometerTypeShort'),
                        first_entry_date=datetime.strptime(json_filename.split('_')[2] + '_' + json_filename.split('_')[3].split('.')[0], '%Y%m%d_%H%M%S'),
                        photos_count=len(vehicle.get('VehiclePhotos', [])),
                        active=True,
                        OptionCodeList=vehicle.get('OptionCodeList')
                    )
                    session.add(car)
                    session.flush()
                else:
                    car.active = True
                    car.last_updated = datetime.utcnow()
                    car.photos_count = len(vehicle.get('VehiclePhotos', []))

                # Process variable data (e.g., price changes)
                price = Prices(
                    car_id=car.id,
                    price=vehicle.get('InventoryPrice', 0.0),
                    date=timestamp
                )
                session.add(price)

                # Process photos with uniqueness check
                vehicle_photos = vehicle.get('VehiclePhotos', [])
                for photo in vehicle_photos:
                    image_url = photo.get('imageUrl')
                    if image_url:
                        # Prüfen, ob das Foto bereits vorhanden ist
                        existing_photo = session.query(Photos).filter_by(car_id=car.id, image_url=image_url).first()
                        if not existing_photo:
                            photo_entry = Photos(
                                car_id=car.id,
                                image_url=image_url
                            )
                            session.add(photo_entry)

            # Setzen Sie den active-Status auf False für Fahrzeuge, die nicht in der aktuellen Liste sind
            cars_to_deactivate = session.query(Cars).filter(Cars.vin.notin_(processed_vins), Cars.active == True).all()
            for car_to_deactivate in cars_to_deactivate:
                car_to_deactivate.active = False
                car_to_deactivate.last_updated = datetime.utcnow()

            # Process model stats and pass the timestamp from the filename
            process_model_stats(session, data, timestamp)

            # Commit der Änderungen
            session.commit()

    except Exception as e:
        logger.error(f"Fehler beim Verarbeiten der JSON-Datei: {e}")

def get_wltp_range(vehicle):
    option_code_specs = vehicle.get('OptionCodeSpecs', {})
    c_specs = option_code_specs.get('C_SPECS', {})
    options = c_specs.get('options', [])
    
    for option in options:
        if option.get('code') == 'SPECS_RANGE' and 'WLTP' in option.get('description', ''):
            return option.get('name', '')
    
    return ''  # Return an empty string if no WLTP range is found


        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        logger.error("Usage: python add_cars_2db.py <json_filename>")
        sys.exit(1)

    json_filename = sys.argv[1]
    process_json_file(json_filename)
    # extract_date_from_filename(json_filename)

logger.info("Skript wurde erfolgreich ausgeführt.")