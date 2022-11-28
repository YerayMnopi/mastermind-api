from uuid import uuid4

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        MetaData, String, Table)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql import func

from src.domain.game import Game, Guess

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

guesses = Table(
    "guesses",
    metadata,
    Column("identifier", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("game_id", UUID(as_uuid=True), ForeignKey('games.identifier')),
    Column("code", String(Game.code_length)),
    Column("black_peqs", Integer, default=0),
    Column("white_peqs", Integer, default=0),
    Column("date_created", DateTime(timezone=True), server_default=func.now()),
)


def start_mappers():
    mapper(Game, games, properties={
        'guesses': relationship(Guess, backref='game', cascade="all,delete", lazy="joined")
    })
    mapper(Guess, guesses)
