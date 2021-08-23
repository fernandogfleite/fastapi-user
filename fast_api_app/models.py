from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Float

from fast_api_app.database import Base
from fastapi_users.db.sqlalchemy import GUID, SQLAlchemyBaseUserTable


class UserTable(Base, SQLAlchemyBaseUserTable):
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    owner_id = Column(GUID, ForeignKey("user.id"))
    owner = relationship("UserTable", back_populates="items")
