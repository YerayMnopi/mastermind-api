FROM python:3.10.8-slim as base
ENV PYTHONUNBUFFERED 1

RUN apt-get update&& apt-get install -y \
	&& rm -fr /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install -U pip setuptools wheel
RUN pip3 install pdm
RUN pdm config python.use_venv false

RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

FROM base as build
COPY pyproject.toml pdm.lock ./
USER root

RUN pdm sync --prod

FROM base

COPY --chown=app --from=build /home/app/__pypackages__ /home/app/__pypackages__
COPY --chown=app src ./src
COPY --chown=app alembic ./alembic

COPY --chown=app .env ./
COPY --chown=app alembic.ini ./
COPY --chown=app pyproject.toml pdm.lock  ./

EXPOSE 8000


ENV PYTHONPATH=/home/app/__pypackages__/3.10/lib


