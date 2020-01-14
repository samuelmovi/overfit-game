# class models required for server functioning
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///../overfit-server.db', echo=True)


class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    winner = Column(String(25), nullable=False)
    loser = Column(String(25), nullable=False)
    timestamp = Column(String(30), nullable=False)
    
    def __repr__(self):
        return f'<Match(id={self.id}, winner={self.winner}, loser={self.loser}, timestamp={self.timestamp}'


Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
import datetime


class Db:
    
    def __init__(self):
        try:
            # self.engine = create_engine('sqlite://overfit-server.db', echo=True)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            
        except Exception as e:
            print(f'[!!] Error opening database: {e}')
    
    def load_matches(self):
        return self.session.query(Match).limit(10).order_by('timestamp')
    
    def save_match(self, winner, loser):
        new_match = Match(winner=winner, loser=loser, timestamp=str(datetime.datetime.now()))
        self.session.add(new_match)
        self.session.commit()

