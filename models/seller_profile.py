from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import BaseTableModel

class SellerProfile(BaseTableModel):
    __tablename__ = "seller_profiles"

    user_uuid = Column(String, ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False, unique=True)

    store_name = Column(String, nullable=False)
    store_logo = Column(String, nullable=True)
    store_logo_id = Column(String, nullable=True)
    business_address = Column(String, nullable=True)
    business_category = Column(String, nullable=True)
    store_description = Column(String, nullable=True)

    verified = Column(Boolean, default=False)
    ratings = Column(Float, default=0.0)  
    total_sales = Column(Integer, default=0) 

    # Social media links
    facebook = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    instagram = Column(String, nullable=True)
    
    # Relationship back to user
    user = relationship("User", back_populates="seller_profile")
    addresses = relationship("Address", back_populates="seller_profile", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SellerProfile store_name={self.store_name} user_uuid={self.user_uuid}>"
