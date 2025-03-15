from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    uuid : str
    name: str 
    email: EmailStr	
    password: Optional[str]	
    google_sub: Optional[str] 
    is_active: bool 
    role: str 
    is_superuser: bool 
    is_verified: bool  


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr	
    password: str


class UserLogin(BaseModel):
    email: EmailStr	
    password: str	


class TokenData(BaseModel):
    """Schema to structure token data"""
    id: Optional[str]
    