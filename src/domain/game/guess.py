from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass()
class Guess:
    identifier: UUID
    game_id: UUID
    code: str
    black_peqs: int
    white_peqs: int
    date_created: datetime
