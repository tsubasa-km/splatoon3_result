from models.weapon import Weapon
from models.team import Team
from models.sub_weapon import SubWeapon
from models.stage import Stage
from models.special_weapon import SpecialWeapon
from models.player import Player
from models.game import Game
from models.base import Base
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


engine = create_engine("sqlite:///database.db", echo=True)

if not os.path.exists("database.db"):
    Base.metadata.create_all(engine)
