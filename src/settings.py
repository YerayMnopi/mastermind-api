import logging.config
from functools import lru_cache
from logging import Logger

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """
    Main Configuration of the whole app.
    """
    postgres_host: str
    postgres_port: int
    postgres_password: str
    postgres_username: str
    postgres_database: str
    app_port: int
    app_host: str

    class Config:
        env_file = ".env"

    def get_postgres_uri(self) -> PostgresDsn:
        auth = f"{self.postgres_username}:{self.postgres_password}"
        address = f"{self.postgres_host}:{self.postgres_port}/{self.postgres_database}"
        return f"postgresql://{auth}@{address}"

    def get_api_url(self):
        return f"http://{self.app_host}:{self.app_port}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


MY_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },
    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },
    'loggers': {
        'mylogger': {
            'handlers': ['stream_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

logging.config.dictConfig(MY_LOGGING_CONFIG)


@lru_cache()
def get_logger() -> Logger:
    return logging.getLogger('mylogger')
