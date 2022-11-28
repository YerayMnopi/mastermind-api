from typing import Any
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.application import (CreateGameHandler, CreateGameRequest,
                             GetGameHandler, GetGameRequest, GuessCodeHandler,
                             GuessCodeRequest)
from src.domain.game import (GameColor, InvalidGuessValuesException,
                             MaxTriesReachedException)
from src.infrastructure.data import (PostgresGamesUnitOfWork,
                                     PostgresqlGamesRepository)

from ..data.mappers import start_mappers
from .dto import CreateGamePayload, GameResponse, GuessPayload

start_mappers()


app: Any = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/games", status_code=201, response_model=GameResponse)
async def create(body: CreateGamePayload):
    uow = PostgresGamesUnitOfWork()
    request = CreateGameRequest(max_tries=body.max_tries)
    game = CreateGameHandler(uow).handle(request)

    return vars(game)


@app.get("/games/{identifier}", response_model=GameResponse)
async def get(identifier: UUID):
    repo = PostgresqlGamesRepository()
    request = GetGameRequest(identifier=identifier)
    game = GetGameHandler(repo).handle(request)

    return vars(game)


@app.post("/games/{identifier}/guess", status_code=201, response_model=GameResponse)
async def create_guess(identifier: UUID, guess: GuessPayload):
    uow = PostgresGamesUnitOfWork()
    request = GuessCodeRequest(
        identifier=identifier,
        guess=guess.code
    )
    try:
        game = GuessCodeHandler(uow).handle(request)
    except InvalidGuessValuesException as exc:
        allowed_values = ', '.join([item.value for item in GameColor])
        raise HTTPException(
            status_code=400,
            detail=f"Invalid code values. Allowed values are {allowed_values}"
        ) from exc
    except MaxTriesReachedException as exc:
        raise HTTPException(
            status_code=400, detail="GAME OVER. Max tries reached.") from exc

    return vars(game)
