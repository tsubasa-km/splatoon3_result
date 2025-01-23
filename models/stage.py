from sqlalchemy import Column, Integer, String

from models.base import Base


class Stage(Base):
    __tablename__ = "stages"
    id = Column(Integer, primary_key=True)
    name = Column(String)
