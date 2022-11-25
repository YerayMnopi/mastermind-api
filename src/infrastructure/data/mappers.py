from uuid import uuid4

from sqlalchemy import (Boolean, Column, DateTime, Integer, MetaData, String,
                        Table, create_engine)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import func

from src.domain.game import Game
from src.settings import get_settings

metadata = MetaData()

games = Table(
    "games",
    metadata,
    Column("identifier", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("code", String(Game.code_length)),
    Column("max_tries", Integer, default=Game.default_max_tries),
    Column("tries", Integer, default=0),
    Column("guessed", Boolean, default=False),
    Column("date_created", DateTime(timezone=True), server_default=func.now()),
    Column("date_modified", DateTime(timezone=True), onupdate=func.now()),
)


def start_mappers():
    mapper(Game, games)


get_session = sessionmaker(bind=create_engine(
    get_settings().get_postgres_uri()))
