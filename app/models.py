from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cell(Base):
    __tablename__ = "cells"

    x = Column(Integer, primary_key=True)
    y = Column(Integer, primary_key=True)
    content = Column(String(256))

    def __repr__(self):
        return f"Cell(x={self.x!r}, y={self.y!r}, content={self.content!r})"


class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True)
