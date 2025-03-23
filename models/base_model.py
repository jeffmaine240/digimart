from uuid import uuid4
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, func




# ====== Declarative Base ====== #
Base = declarative_base()



class BaseTableModel(Base):

    __abstract__ = True
    
    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now())
    

    
    def save(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    def delete(self, db: Session):
        db.delete(self)
        db.commit()

    def update(self, db: Session, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.commit()
        db.refresh(self)
        return self

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column('user_id', ForeignKey('users.uuid'), primary_key=True),
    Column('role_id', ForeignKey('roles.uuid'), primary_key=True)
)