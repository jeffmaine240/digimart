from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import BaseTableModel


class Profile(BaseTableModel):
    __tablename__ = "profiles"
    user_uuid = Column(String, ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)
    bio = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    avatar_id = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    # Relationships one-to-one user
    user = relationship("User", back_populates="profile")

    # Relationships one-to-many addresses
    addresses = relationship("Address", back_populates="profile", cascade="all, delete-orphan")