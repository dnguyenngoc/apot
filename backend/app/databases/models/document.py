from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from databases.db import Base

    
class Document(Base):
    __tablename__ = "document"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    export_date = Column(DateTime, nullable=True, default=None)
    create_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=True, default=None)
    type_id = Column(Integer,ForeignKey('document_type.id'), nullable=False)
    
    type = relationship('DocumentType', lazy = 'noload', foreign_keys=[type_id])
   