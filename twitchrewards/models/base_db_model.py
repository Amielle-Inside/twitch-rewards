"""Base class for classes using sqlalchemy's ORM"""

from dataclasses import dataclass

from sqlalchemy.orm import DeclarativeBase


@dataclass
class Base(DeclarativeBase):
    """Base class for classes using sqlalchemy's ORM"""
