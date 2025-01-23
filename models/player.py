from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from models.base import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    weapon_id = Column(Integer, ForeignKey('weapons.id'))
    kill = Column(Integer)
    death = Column(Integer)
    assist = Column(Integer)
    special = Column(Integer)
    splat_point = Column(Integer)
    power = Column(Integer)
    is_me = Column(Boolean)