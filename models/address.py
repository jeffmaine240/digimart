from sqlalchemy import Boolean, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import BaseTableModel

class Address(BaseTableModel):
    __tablename__ = "addresses"

    profile_id = Column(String, ForeignKey("profiles.uuid", ondelete="CASCADE"), nullable=True)
    seller_profile_id = Column(String, ForeignKey("seller_profiles.uuid", ondelete="CASCADE"), nullable=True)

    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    postal_code = Column(String, nullable=True)
    is_default = Column(Boolean, default=False)

    # Relationships
    profile = relationship("Profile", back_populates="addresses")
    seller_profile = relationship("SellerProfile", back_populates="addresses")

