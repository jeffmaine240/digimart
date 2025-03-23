from datetime import timedelta, timezone, datetime
from sqlalchemy import Column, DateTime, String, Boolean, Enum, event
from sqlalchemy.orm import relationship
from .base_model import BaseTableModel, user_roles
from enum import Enum as PyEnum


# ====== Enum for Role Management ====== #

class Role(BaseTableModel):
    __tablename__ = "roles"

    # === Fields === #
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True) 

    # Relationship to users (many-to-many)
    users = relationship("User", secondary=user_roles, back_populates="roles")
    
    def __repr__(self):
        return f"<Role {self.name}>"