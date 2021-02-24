import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Binary
from sqlalchemy import orm
from sqlalchemy.orm import relationship

class Gamer(SqlAlchemyBase):
    __tablename__ = "gamers"
    id = Column(Integer, primary_key=True)
    guessed_words = relationship("Word", back_populates="gamers")

class Word(SqlAlchemyBase):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    guesses_number = Column(Integer)
    accent_position = Column(Integer)
    word_structure = Column(String)
    text = Column(String)
    gamer_id = Column(Integer, ForeignKey("gamers.id"))
    gamers = relationship("Gamer", back_populates="guessed_words")
    

    
