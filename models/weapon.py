from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey

from models.base import Base


class Weapon(Base):
    __tablename__ = "weapons"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    sub_weapon_id = Column(Integer, ForeignKey("sub_weapons.id"))
    special_weapon_id = Column(Integer, ForeignKey("special_weapons.id"))
    icon = Column(LargeBinary)
