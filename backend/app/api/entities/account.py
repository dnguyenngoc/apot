# Python class represent the entities
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import List


class Token(BaseModel):
    token_type: Optional[str] = 'bearer'
    access_token: Optional[str]
    refresh_token: Optional[str]
    expire_token: Optional[datetime]
    expire_refresh_token: Optional[datetime]
    role_name: Optional[list]


class TokenCreate(BaseModel):
    user_name: Optional[str]
    password: Optional[str]
    role_id: Optional[List]
    role_name: Optional[List]


class TokenPayload(BaseModel):
    user_name: Optional[str]
    password: Optional[str]
    role_id: Optional[List]
    role_name: Optional[List]