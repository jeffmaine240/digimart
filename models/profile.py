from sqlalchemy import Column, Date, Enum, String, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import BaseTableModel
from enum import Enum as PyEnum



# ===== Optional Enum for Gender ===== #
class GenderEnum(PyEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class Profile(BaseTableModel):
    __tablename__ = "profiles"
    user_uuid = Column(String, ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False, unique=True)
    bio = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    avatar_id = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    facebook = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    instagram = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)

    # Relationships one-to-one user
    user = relationship("User", back_populates="profile")

    # Relationships one-to-many addresses
    addresses = relationship("Address", back_populates="profile", cascade="all, delete-orphan")