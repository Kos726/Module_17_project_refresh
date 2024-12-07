from typing import ClassVar

from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(url="sqlite:///taskmanager.db", echo=True)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    __table__: ClassVar[Table]
