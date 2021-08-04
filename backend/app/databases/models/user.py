from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Boolean, DECIMAL
from databases.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), nullable=False, index=True,  unique=True)
    first_nane = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    full_nane = Column(String(500), nullable=False)
    email = Column(String(500), nullable=False)
    phone = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role_id =  Column(Integer, ForeignKey('role.id'), nullable=False)
    create_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=True, default=None)
    role = relationship('Role', lazy = 'noload', foreign_keys=[role_id])