from sqlalchemy import Column, String, Boolean
from pydantic import EmailStr
from typing import Optional


from .base_model import BaseTableModel

class User(BaseTableModel):
    __tablename__ = "users"
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)
    role = Column(String, nullable=False, default="user")
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    google_sub = Column(String, nullable=True)
    is_google_acct = Column(Boolean, default=False)

    

    def __repr__(self):
        return f"<User {self.email}>"
    

    def __str__(self):
        return self.email