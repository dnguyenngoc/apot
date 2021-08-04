# Python class represent the entities
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


# Shared properties
class UserBase(BaseModel):
    user_name: Optional[str]
    first_nane: Optional[str]
    last_name: Optional[str]
    full_nane: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    password: Optional[str]
    role_id: Optional[int]
    create_date: Optional[datetime]
    update_date: Optional[datetime] = None
    class Config:
        orm_mode = True

class UserInDB(UserBase):
    id: Optional[int]

class UserCreate(BaseModel):
    user_name: Optional[str]
    first_nane: Optional[str]
    last_name: Optional[str]
    full_nane: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    password: Optional[str]
    role_id: Optional[int]
    create_date: Optional[datetime]