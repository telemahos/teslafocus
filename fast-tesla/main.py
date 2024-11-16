from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional ,Dict
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.orm import Session
from datetime import datetime, date
import traceback
import logging


# On video 3:30
# TODO
# repository/delete problem
# FastAPI-Anwendung initialisieren
app = FastAPI()

# Füge CORS Middleware hinzu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://phphidmlnlniokffpoehdcpkanccmfmj"],  # Erlaube alle Ursprünge, passe dies nach Bedarf an
    allow_credentials=True,
    allow_methods=["*"],  # Erlaube alle Methoden
    allow_headers=["*"],  # Erlaube alle Header
)

# Datenbank-Setup
DATABASE_URL = "sqlite:///./tesla_inventory.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



class Prices(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    price = Column(Float)
    date = Column(DateTime)

    car = relationship("Cars", back_populates="prices")

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

    prices = relationship("Prices", back_populates="car")

# Definiere das Datenbankmodell für die IDs
class IdModel(Base):
    __tablename__ = "ids"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Erstelle die Tabellen in der Datenbank
Base.metadata.create_all(bind=engine)

# Pydantic-Modell für die Anfrage
class IdList(BaseModel):
    ids: List[str]

# Pydantic-Modell für die Anfrage
class VinList(BaseModel):
    vins: List[str]

# Pydantic-Modell für die Antwort
class CarResponse(BaseModel):
    vin: str
    factory_gated_date: Optional[date]
    model: str
    trim: Optional[str]
    odometer: Optional[int]
    vehicle_history: Optional[str]
    photos_count: Optional[int]
    first_entry_date: Optional[date]
    days_in_stock: Optional[int]
    heatpump: Optional[bool]
    factory: Optional[str]
    battery_capacity: Optional[float] = Field(default=None)
    min_price: Optional[float]
    max_price: Optional[float]
    avg_price: Optional[float]
    price_difference: Optional[float]
    price_trend: Optional[str]  # Das Plus- oder Minuszeichen
    current_price: Optional[float]

class CarsResponse(BaseModel):
    cars: List[CarResponse]

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_price_stats(db: Session, car_ids: List[int]) -> Dict[int, Dict[str, Optional[float]]]:
    price_stats = {}
    
    for car_id in car_ids:
        # Get the latest price for the car
        latest_price_subquery = (
            db.query(Prices)
            .filter(Prices.car_id == car_id)
            .order_by(Prices.date.desc())
            .limit(1)
            .subquery()
        )

        stats = db.query(
            func.min(Prices.price).label('min_price'),
            func.max(Prices.price).label('max_price'),
            func.avg(Prices.price).label('avg_price'),
            (func.max(Prices.price) - func.min(Prices.price)).label('price_difference'),
            latest_price_subquery.c.price.label('current_price')  # Get the current price from the subquery
        ).outerjoin(
            latest_price_subquery,
            latest_price_subquery.c.car_id == car_id
        ).filter(Prices.car_id == car_id).first()

        if stats:
            price_stats[car_id] = {
                'min_price': float(stats.min_price) if stats.min_price is not None else None,
                'max_price': float(stats.max_price) if stats.max_price is not None else None,
                'avg_price': float(stats.avg_price) if stats.avg_price is not None else None,
                'price_difference': float(stats.price_difference) if stats.price_difference is not None else None,
                'current_price': float(stats.current_price) if stats.current_price is not None else None
            }
        else:
            price_stats[car_id] = {
                'min_price': None,
                'max_price': None,
                'avg_price': None,
                'price_difference': None,
                'current_price': None
            }
    
    return price_stats

# Helper function to format price difference
def get_price_trend(price_diff):
    if price_diff > 0:
        return "-"
    elif price_diff < 0:
        return "+"
    return ""

# POST-Route zum Empfangen der IDs
@app.post("/ids/")
async def receive_ids(id_list: IdList, db: Session = Depends(get_db)):
    ids = id_list.ids
    
    try:
        # Prüfe, ob die IDs bereits existieren
        existing_ids = {id_.id for id_ in db.query(IdModel).filter(IdModel.id.in_(ids)).all()}
        
        # Filtere nur die IDs, die noch nicht vorhanden sind
        new_ids = [id_ for id_ in ids if id_ not in existing_ids]
        
        # Füge neue IDs zur Datenbank hinzu
        if new_ids:
            db.bulk_insert_mappings(IdModel, [{"id": id_, "timestamp": datetime.utcnow()} for id_ in new_ids])
            db.commit()

        # Call search_cars method
        vin_list = VinList(vins=ids)  # Assuming IDs are VINs
        cars_response = await search_cars(vin_list, db)
        
        response = {
            "received_ids": ids,
            "cars": cars_response.dict()["cars"]
        }
        
        print(response)  # Ausgabe der Antwort
        return response
    
    except Exception as e:
        db.rollback()
        error_msg = f"Error processing request: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # This will print the full stack trace to your console
        raise HTTPException(status_code=500, detail=error_msg)

# POST-Route zum Suchen der Autos anhand der VIN-Nummern
@app.post("/search_cars/", response_model=CarsResponse)
async def search_cars(vin_list: VinList, db: Session = Depends(get_db)):
    if not vin_list:
        raise HTTPException(status_code=400, detail="VIN-Liste darf nicht leer sein")

    vins = vin_list.vins
    
    try:
        # Suche nach Autos mit den gegebenen VIN-Nummern
        cars = db.query(Cars).filter(Cars.vin.in_(vins)).all()
        
        if not cars:
            raise HTTPException(status_code=404, detail="Keine Autos mit den angegebenen VIN-Nummern gefunden")
        
        # Hole die Preis-Statistiken für alle gefundenen Autos
        car_ids = [car.id for car in cars]
        price_stats = get_price_stats(db, car_ids)
        
        # Erstelle die Antwort
        response = CarsResponse(cars=[
            CarResponse(
                vin=car.vin,
                factory_gated_date=to_date(car.factory_gated_date),
                model=car.model,
                trim=car.trim,
                odometer=car.odometer,
                vehicle_history=car.vehicle_history,
                photos_count=car.photos_count,
                first_entry_date=to_date(car.first_entry_date),
                days_in_stock=await get_days_on_stock(car.first_entry_date),
                heatpump=await get_heatpump(car.factory_gated_date),
                factory=await get_factory(car.vin),
                battery_capacity=car.battery_capacity,
                min_price=price_stats[car.id]['min_price'],
                max_price=price_stats[car.id]['max_price'],
                avg_price=price_stats[car.id]['avg_price'],
                price_difference=price_stats[car.id]['price_difference'],
                price_trend=get_price_trend(price_stats[car.id]['price_difference']),
                current_price=price_stats[car.id]['current_price']
            ) for car in cars
        ])
        
        print(response)  # Ausgabe der Antwort
        return response
    except HTTPException as http_exc:
        # Fange HTTP Exceptions und gebe sie direkt zurück
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Verarbeiten der Anfrage: {str(e)}")


async def get_days_on_stock(first_entry_date): 
    # Überprüfen, ob first_entry_date None ist
    if first_entry_date is None:
        return "Today"  # oder einen anderen geeigneten Wert, der in deinem Anwendungsfall Sinn macht

    # Holen Sie sich das heutige Datum
    today = datetime.now()

    # Berechne die Differenz zwischen den beiden Daten
    difference = today - first_entry_date

    # Anzahl der Tage aus der Differenz extrahieren
    days_difference = difference.days
    print(f"Anzahl der Tage seit dem gegebenen Datum: {days_difference}")
    return days_difference


async def get_heatpump(factory_gated_date):
    # Überprüfen, ob das Herstellungsdatum None ist
    if factory_gated_date is None:
        return False  # Oder eine andere geeignete Handhabung für diesen Fall

    # Definiere das Datum, ab dem Wärmepumpen eingeführt wurden
    heatpump_cutoff_date = datetime(2020, 10, 1)

    # Überprüfen, ob das Herstellungsdatum nach dem Cutoff-Datum liegt
    if factory_gated_date >= heatpump_cutoff_date:
        return True  # Wärmepumpe vorhanden
    else:
        return False  # Wärmepumpe nicht vorhanden
    
async def get_factory(vin):
    try:
        # Überprüfen, ob die VIN gültig ist
        if not isinstance(vin, str) or len(vin) < 8:
            return None  # oder eine geeignete Fehlerbehandlung

        # Bestimme die Herstellungsfabrik anhand der siebten Stelle vor dem Ende
        factory_code = vin[-7]  # Siebte Stelle von hinten
        
        if factory_code == 'F':
            return "Fremont"
        elif factory_code == 'C':
            return "China"
        elif factory_code == 'B':
            return "Berlin"
        else:
            return "Unbekannte Fabrik"  # Für andere Codes
    
    except Exception as e:
        logging.error(f"Fehler beim Durchsuchen der Autos: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Fehler beim Verarbeiten der Anfrage: {str(e)}")
    
# Helper function to convert datetime to date
def to_date(datetime_value):
    if datetime_value:
        return datetime_value.date()
    return None