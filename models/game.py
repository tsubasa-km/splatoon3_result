from sqlalchemy import Column, Integer, String, ForeignKey

from models.base import Base


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    rule = Column(String, nullable=False)
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=False, index=True)
    datetime = Column(String, nullable=False, index=True)
    time = Column(Integer, nullable=False)
    source_image_hash = Column(String(64), unique=True, nullable=True)
