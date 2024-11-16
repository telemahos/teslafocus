from typing import List
from fastapi import APIRouter, Depends, status
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from ..mvc import case, user, cars

router = APIRouter(
    prefix="/api/cars",
    tags=['Cars']
)

get_db = database.get_db

@router.get('/', response_model=List[schemas.ShowCase]) 
async def all_cars(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return cars.cars_get_all(db)