from typing import Dict, List, Optional
from ..schemas import IdList, VinList, CarsResponse, CarResponse
from ..models import IdModel, Cars, Prices
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2
from datetime import datetime
from ..mvc import case, user, cars
from ..mvc.cars import get_price_stats, get_price_trend, to_date, get_factory, get_heatpump, get_days_on_stock
import traceback
import logging

router = APIRouter(
    prefix="/api/cars",
    tags=['Cars']
)

logger = logging.getLogger(__name__)

get_db = database.get_db

@router.get('/', response_model=List[schemas.ShowCase]) 
async def all_cars(db: Session = Depends(get_db)):
    return cars.cars_get_all(db)

# POST-Route zum Empfangen der IDs
@router.post("/ids/")
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
@router.post("/search_cars/", response_model=CarsResponse)
async def search_cars(vin_list: VinList, db: Session = Depends(get_db)):
    logger.info(f"Suche nach Autos mit VINs: {vin_list}")
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
        logger.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.exception("Ein unbekannter Fehler ist aufgetreten")
        raise HTTPException(status_code=500, detail=f"Fehler beim Verarbeiten der Anfrage: {str(e)}")


