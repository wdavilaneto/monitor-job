from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey

Base = declarative_base()


class Board(Base):
    # __tablename__ = 'board'
    __tablename__ = 'portfolio_board'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sid = Column(String(200), unique=True, nullable=False)
    name = Column(String(200), unique=True, nullable=False)
    last_update = Column(DateTime(timezone=True), onupdate=func.now())
    hide = Column(Boolean, default=False)
    def __repr__(self):
        return '<Task {}>'.format(self.name)


class Task(Base):
    __tablename__ = 'portfolio_task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trello_id = Column(Integer)
    name = Column(Text, nullable=True)
    label = Column(String(200))
    cycle_time = Column(Integer)
    lead_time = Column(Integer)
    created = Column(Date)
    start = Column(Date)
    end = Column(Date)
    friday = Column(Date)
    card_url = Column(String(300), nullable=True)
    board_id = Column(Integer)


    def __repr__(self):
        return '<Task {}, {}>'.format(self.trello_id, self.board_id)
