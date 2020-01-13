# class models required for server functioning
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import create_engine, ForeignKey

Base = declarative_base()
engine = create_engine('sqlite://overfit-server.db', echo=True)


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    token = Column(String(10))     # player'd id string
    playing = Column(Boolean, default=False)
    available = Column(Boolean, default=False)
    top_score = Column(Integer, default=0)
    
    def __repr__(self):
        return f'<Player(id={self.id}, active={self.active}, ' \
            f'playing={self.playing}, ' \
            f'available={self.available}, ' \
            f'top_score={self.top_score}'


class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    player_1 = Column(Integer, ForeignKey('player.id'), nullable=False)
    player_2 = Column(Integer, ForeignKey('player.id'), nullable=False)
    top_score = Column(Integer, default=0)
    timestamp = Column()
    
    def __repr__(self):
        return f'<Match(id={self.id}, timestamp={self.timestamp}'


Base.metadata.create_all(engine)
