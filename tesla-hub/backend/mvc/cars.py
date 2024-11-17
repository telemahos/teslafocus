from typing import List, Dict, Optional
from ..models import Prices
from sqlalchemy.orm import Session
# from .. import schemas, models
from sqlalchemy.sql import text, func
from sqlalchemy import desc
from datetime import datetime
from fastapi import HTTPException
import logging

# Show All issue ##.order_by(desc('date'))
def cars_get_all(db: Session, limit: int = 10, offset: int = 0 ):
    cars = db.query(models.Cars).offset(offset).limit(limit).all()
    return cars

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


# ------------------------------------------
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