from src.db.database import Base
from uuid import uuid4
from sqlalchemy import Column, DateTime, Integer, String, func

class BaseTableModel(Base):

    __abstract__ = True
    
    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now())