# class models required for server functioning
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import create_engine, ForeignKey

Base = declarative_base()
engine = create_engine('sqlite://overfit-server.db', echo=True)


class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    winner = Column(String(25), nullable=False)
    loser = Column(String(25), nullable=False)
    timestamp = Column(String(30), nullable=False)
    
    def __repr__(self):
        return f'<Match(id={self.id}, winner={self.winner}, loser={self.loser}, timestamp={self.timestamp}'


Base.metadata.create_all(engine)
