from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from models.base import Base


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    color = Column(String, nullable=False)
    is_winner = Column(Boolean, nullable=False)
    score = Column(Integer)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False, index=True)
