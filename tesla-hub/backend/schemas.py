from typing import List, Optional, Union
from datetime import date
# datetime, time
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# User
# ------------------------------------
class User(BaseModel):
    id: int
    name: str
    email: str
    password: Union[str, None] = None
    user_role: int

class ShowUser(BaseModel):
    id: int
    name: Union[str, None] = None 
    email: Union[str, None] = None
    user_role: Union[int, None] = None
    class Config():
        orm_mode = True


# Case
# ------------------------------------
class CaseBase(BaseModel):
    id: int
    case_nr: Optional[str] = None
    start_date: Optional[date]
    due_date: Optional[date]
    title: Optional[str] = None
    description: Optional[str] = None
    tags:  Optional[str] = None
    status:  Optional[int] = 0
    priority: Optional[int] = 0
    case_type: Optional[int] = 0
    project_id: Optional[int] = None
    owner_id: Optional[int] = None

class Case(CaseBase):
    class Config():
        orm_mode = True

class ShowCase(CaseBase):
    id: int
    case_nr: Optional[str] = None
    start_date: Optional[date]
    due_date: Optional[date]
    title: Optional[str] = None
    description: Optional[str] = None
    tags:  Optional[str] = None
    status:  Optional[int] = 0
    priority: Optional[int] = 0
    case_type: Optional[int] = 0
    project_id: Optional[int] = None
    owner_id: Optional[int] = None

    class Config():
        orm_mode = True
    
# Project
# ------------------------------------
class ProjectBase(BaseModel):
    id: int
    project_nr: Optional[str] = None
    start_date: date
    due_date : date
    title: Optional[str] = None
    description: Optional[str] = None
    tags:  Optional[str] = None
    active:  Optional[bool] = False
    status:  Optional[int] = 0
    priority: Optional[int] = 0
    owner_id: Optional[int] = None

class Project(ProjectBase):
    class Config():
        orm_mode = True

class ShowProject(ProjectBase):
    id: int
    project_nr: Optional[str] = None
    start_date: date
    due_date : date
    title: Optional[str] = None
    description: Optional[str] = None
    tags:  Optional[str] = None
    active:  Optional[bool] = False
    status:  Optional[int] = 0
    priority: Optional[int] = 0
    owner_id: Optional[int] = 0

    class Config():
        orm_mode = True
        
# TeamMembers
# ------------------------------------
class TeamMemberBase(BaseModel):
    id: int
    project_id: int 
    user_id: int
    team_role: Optional[int] = 0
    assign_date: date
    active:  Optional[bool] = True
    note:  Optional[str] = None
    
class TeamMember(TeamMemberBase):
    class Config():
        orm_mode = True
        
class ShowTeamMember(TeamMemberBase):
    id: int
    project_id: int 
    user_id: int
    team_role: Optional[int] = 0
    assign_date: date
    active:  Optional[bool] = True
    note:  Optional[str] = None

    class Config():
        orm_mode = True


# Cars
# ------------------------------------
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

    class Config():
        orm_mode = True

class CarsResponse(BaseModel):
    cars: List[CarResponse]