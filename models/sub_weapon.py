from sqlalchemy import Column, Integer, String

from models.base import Base


class SubWeapon(Base):
    __tablename__ = "sub_weapons"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
