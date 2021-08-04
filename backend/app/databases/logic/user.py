from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload, raiseload

from databases.models.user import User
from databases.models.role import Role
from databases.models.user_role import UserRole

from datetime import datetime


def get_user_by_user_name_and_password_join_role(db_session: Session, user_name: str, password: str) -> User:
     return db_session.query(User) \
                     .options(joinedload('role')) \
                     .filter(User.user_name == user_name, 
                             User.password == password) \
                     .first()

def get_user_by_email_and_password_join_role(db_session: Session, email: str, password: str) -> User:
     return db_session.query(User) \
                     .options(joinedload('role')) \
                     .filter(User.email == email, 
                             User.password == password) \
                     .first()

def get_user_by_user_id_and_user_name_and_email_and_role_id_join_role(
     db_session: Session, user_id: str, user_name: str, email: str, role_id: int
) -> User:
     return db_session.query(User) \
                     .options(joinedload('role')) \
                     .filter(User.id == user_id,
                             User.user_name == user_name, 
                             User.email == email,
                             User.role_id == role_id) \
                     .first()

def get_user_role_by_name(db_session: Session, user_name: str) -> UserRole:
    return db_session.query(UserRole) \
                     .filter(UserRole.user_name == user_name) \
                     .all()