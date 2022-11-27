from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.settings import get_settings

get_session: Session = sessionmaker(bind=create_engine(
    get_settings().get_postgres_uri()))
