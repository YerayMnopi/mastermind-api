from typing import Any
from uuid import UUID

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.application import (CreateGameHandler, CreateGameRequest,
                             GetGameHandler, GetGameRequest, GuessCodeHandler,
                             GuessCodeRequest)
from src.infrastructure.data import (PostgresGamesUnitOfWork,
                                     PostgresqlGamesRepository)

from ..data.mappers import start_mappers

start_mappers()


app: Any = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/games", status_code=201)
async def create():
    uow = PostgresGamesUnitOfWork()
    request = CreateGameRequest()
    game = CreateGameHandler(uow).handle(request)

    return game


@app.get("/games/{identifier}")
async def get(identifier: UUID):
    repo = PostgresqlGamesRepository()
    request = GetGameRequest(identifier=identifier)
    game = GetGameHandler(repo).handle(request)

    return game


class Guess(BaseModel):
    code: str


@app.post("/games/{identifier}/guess", status_code=201)
async def create_guess(identifier: UUID, guess: Guess):
    uow = PostgresGamesUnitOfWork()
    request = GuessCodeRequest(
        identifier=identifier,
        guess=guess.code
    )
    game = GuessCodeHandler(uow).handle(request)

    return game
