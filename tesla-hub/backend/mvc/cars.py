import re
import string
import random
from datetime import date
import json
from sqlalchemy.orm import Session
from .. import schemas, models
from fastapi import HTTPException, status
from sqlalchemy.sql import text
from sqlalchemy import desc

# Show All issue ##.order_by(desc('date'))
def cars_get_all(db: Session, limit: int = 10, offset: int = 0 ):
    cars = db.query(models.Cars).offset(offset).limit(limit).all()
    return cars