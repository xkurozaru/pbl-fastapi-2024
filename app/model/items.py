import uuid

from pydantic import BaseModel, ConfigDict
from sqlalchemy import UUID, Column, Integer, String
from ulid import ULID

from app.model.base import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(String(26), primary_key=True)
    name = Column(String(255))
    price = Column(Integer)
    user_id = Column(UUID, nullable=False, index=True)

    def __init__(self, name: str, price: int, user_id: uuid.UUID):
        self.id = str(ULID())
        self.name = name
        self.price = price
        self.user_id = user_id


class ItemSchema(BaseModel):
    id: ULID
    name: str
    price: int

    model_config = ConfigDict(from_attributes=True)
