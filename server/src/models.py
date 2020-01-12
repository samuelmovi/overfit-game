# class models required for server functioning
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'
    
    active = Column(Boolean)
    playing = Column(Boolean)
    available = Column(Boolean)
    top_score = Column(Integer)
    
    def __repr__(self):
        return f'<Player(active={self.active}, ' \
            f'playing={self.playing}, ' \
            f'available={self.available}, ' \
            f'top_score={self.top_score}'


if __name__ == '__main__':
    pass
