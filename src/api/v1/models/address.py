from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import BaseTableModel

class Address(BaseTableModel):
    __tablename__ = "addresses"
    profile_uuid = Column(String, ForeignKey("profiles.uuid", ondelete="CASCADE"), nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)

    # Relationships many-to-one profile
    profile = relationship("Profile", back_populates="addresses")
