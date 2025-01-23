import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from models.base import Base
from models import game, player, special_weapon, stage, sub_weapon, team, weapon

engine = create_engine("sqlite:///database.db", echo=True)

Base.metadata.create_all(engine)
