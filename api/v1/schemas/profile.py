from pydantic import BaseModel, model_validator
from typing import Optional


class UserProfile(BaseModel):
    """Schema to structure user profile data"""
    bio: Optional[str] = None
    phone: Optional[str] = None

    @model_validator(mode="after")
    def check_at_least_one_field(self):
        """
        Ensure that at least one field (bio or phone) is provided.
        """
        if not any([self.bio, self.phone]):
            raise ValueError("At least one field (bio or phone) must be provided")
        return self


