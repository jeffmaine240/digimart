from pydantic import BaseModel


class CreateUserProfile(BaseModel):
    """Schema to structure user profile data"""
    bio: str
    phone: str



