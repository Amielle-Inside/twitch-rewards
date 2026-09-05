"""Handles sqlalchemy abstractions. Provides a method expose a section used to query data"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from twitchrewards.config import settings


def build_connection_string() -> str:
    """
    Build a SQLAlchemy URL based on the environment settings.

    Returns:
        str: The db's connection string.
    """
    return (
        f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )


def get_session_maker() -> sessionmaker:
    """
    Get a session maker that can be used to generate multiple sessions.

    Returns:
        sessionmaker: A maker that can be executed to generate a session.
    """
    connection_string = build_connection_string()
    engine = create_engine(connection_string)
    return sessionmaker(bind=engine)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Get a database session that is closed after usage.

    Returns:
        Session: Database session to execute queries. Closes after context is finished.
    """
    db = _session_maker()
    try:
        yield db
    finally:
        db.close()


_session_maker = get_session_maker()
