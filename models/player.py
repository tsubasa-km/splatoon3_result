from sqlalchemy import Column, Integer, ForeignKey, Boolean

from models.base import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    weapon_id = Column(Integer, ForeignKey("weapons.id"), nullable=False, index=True)
    kill = Column(Integer, nullable=False, default=0)
    death = Column(Integer, nullable=False, default=0)
    assist = Column(Integer, nullable=False, default=0)
    special = Column(Integer, nullable=False, default=0)
    splat_point = Column(Integer, nullable=False, default=0)
    power = Column(Integer)
    is_me = Column(Boolean, nullable=False, default=False)
