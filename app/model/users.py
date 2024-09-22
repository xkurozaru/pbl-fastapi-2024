from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String
from ulid import ULID

from app.model.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String(26), primary_key=True)
    name = Column(String(255))
    grade = Column(Integer)
    team = Column(String(255))

    def __init__(self, name: str, grade: int, team: str):
        self.id = str(ULID())
        self.name = name
        self.grade = grade
        self.team = team


class UserSchema(BaseModel):
    id: ULID
    name: str
    grade: int
    team: str

    model_config = ConfigDict(from_attributes=True)
