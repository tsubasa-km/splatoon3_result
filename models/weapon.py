from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, LargeBinary

Base = declarative_base()

class Weapon(Base):
    __tablename__ = 'weapons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sub_weapon = Column(String)
    special_weapon = Column(String)
    icon = Column(LargeBinary)