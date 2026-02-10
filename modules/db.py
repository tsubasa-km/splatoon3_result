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
from pathlib import Path

from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


DB_PATH = Path(__file__).resolve().parent.parent / "database.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def _table_exists(db_inspector, table_name: str) -> bool:
    return table_name in set(db_inspector.get_table_names())


def _column_exists(db_inspector, table_name: str, column_name: str) -> bool:
    columns = db_inspector.get_columns(table_name)
    return any(column["name"] == column_name for column in columns)


def _all_tables_empty(db_session: Session, existing_tables: set[str]) -> bool:
    for table in Base.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue
        count = db_session.execute(text(f"SELECT COUNT(*) FROM {table.name}")).scalar_one()
        if count > 0:
            return False
    return True


def _try_create_unique_index(db_session: Session, index_name: str, table_name: str, column_name: str):
    try:
        db_session.execute(
            text(
                f"CREATE UNIQUE INDEX IF NOT EXISTS {index_name} "
                f"ON {table_name} ({column_name})"
            )
        )
    except DatabaseError:
        # 既存データに重複がある場合は作成できないため、ここでは処理継続する。
        pass


def _apply_minimum_additive_schema(db_session: Session):
    db_inspector = inspect(db_session.bind)

    if _table_exists(db_inspector, "games") and not _column_exists(
        db_inspector, "games", "source_image_hash"
    ):
        db_session.execute(text("ALTER TABLE games ADD COLUMN source_image_hash VARCHAR(64)"))

    _try_create_unique_index(db_session, "uq_stages_name", "stages", "name")
    _try_create_unique_index(db_session, "uq_weapons_name", "weapons", "name")
    _try_create_unique_index(db_session, "uq_sub_weapons_name", "sub_weapons", "name")
    _try_create_unique_index(
        db_session, "uq_special_weapons_name", "special_weapons", "name"
    )
    _try_create_unique_index(
        db_session, "uq_games_source_image_hash", "games", "source_image_hash"
    )


def initialize_database():
    with Session(engine) as db_session:
        db_inspector = inspect(engine)
        existing_tables = set(db_inspector.get_table_names())

        if not existing_tables:
            Base.metadata.create_all(engine)
            return

        # 既存DBに不足テーブルがある場合は追加作成する。
        Base.metadata.create_all(engine)
        existing_tables = set(inspect(engine).get_table_names())

        if _all_tables_empty(db_session, existing_tables):
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            return

        _apply_minimum_additive_schema(db_session)
        db_session.commit()


initialize_database()
