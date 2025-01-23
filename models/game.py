from sqlalchemy import Column, Integer, String, ForeignKey

from models.base import Base


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    rule = Column(String)
    stage_id = Column(Integer, ForeignKey('stages.id'))
    datetime = Column(String)
    time = Column(Integer)