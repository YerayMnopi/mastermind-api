from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateGamePayload(BaseModel):
    max_tries: int = Field(
        title="Maximun number of guesses a user can do",
        gt=0,
        lt=10
    )


class GuessPayload(BaseModel):
    code: str = Field(
        title="The guess of the user. 4 digits. Available digits: RBOYWG",
        max_length=4,
        min_length=4,
    )


class GuessResponse(BaseModel):
    identifier: UUID
    game_id: UUID
    code: str
    black_peqs: int
    white_peqs: int
    date_created: datetime


class GameResponse(BaseModel):
    date_created: Optional[datetime]
    date_modified: Optional[datetime]
    guesses: Optional[List[GuessResponse]]
    identifier: UUID
    max_tries: int
    tries: int
    guessed: bool
