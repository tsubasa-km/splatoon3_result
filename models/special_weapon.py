from sqlalchemy import Column, Integer, String

from models.base import Base


class SpecialWeapon(Base):
    __tablename__ = "special_weapons"
    id = Column(Integer, primary_key=True)
    name = Column(String)
