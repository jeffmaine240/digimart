from datetime import timedelta, timezone, datetime
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from .base_model import BaseTableModel


class User(BaseTableModel):
    __tablename__ = "users"
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)
    role = Column(String, nullable=False, default="buyer")
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    google_sub = Column(String, nullable=True)
    is_google_acct = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)

    # Relationships one-to-one profile
    profile = relationship("Profile", back_populates="user", cascade="all, delete-orphan", uselist=False)

    def __repr__(self):
        return f"<User {self.email}>"

    def __str__(self):
        return self.email

    def update_last_login(self):
        """Update the user's last login field."""
        self.last_login = datetime.now(timezone(timedelta(hours=1)))