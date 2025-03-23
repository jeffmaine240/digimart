from datetime import timedelta, timezone, datetime
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from .base_model import BaseTableModel, user_roles
from enum import Enum as PyEnum


class User(BaseTableModel):
    __tablename__ = "users"

    # === Fields === #
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=True)  # Nullable to support OAuth users

    # User flags
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_google_acct = Column(Boolean, default=False)

    # For Google OAuth
    google_sub = Column(String, nullable=True)

    # Activity tracking
    last_login = Column(DateTime, nullable=True)

    
    # === Relationships === #

    # Relationship to roles (many-to-many)
    roles = relationship("Role", secondary=user_roles, back_populates="users")

    #one to one relationship to profile
    profile = relationship(
        "Profile", back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    
    #one to one relationship to seller_profile
    seller_profile = relationship(
        "SellerProfile", back_populates="user", cascade="all, delete-orphan", uselist=False
    )

    # === Methods === #
    def __repr__(self):
        return f"<User {self.email}>"

    def __str__(self):
        return self.email

    def update_last_login(self):
        """Update the user's last login field with timezone-aware datetime."""
        self.last_login = datetime.now(timezone(timedelta(hours=1)))

    # Email normalization setter
    @property
    def email_address(self):
        return self.email

    @email_address.setter
    def email_address(self, value: str):
        self.email = value.lower().strip()

