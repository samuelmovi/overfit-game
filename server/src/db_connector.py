from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
# from sqlalchemy import Table,  Column, Integer, String, Boolean
from models import Player, Match
import datetime


class Db:
    
    def __init__(self):
        try:
            self.engine = create_engine('sqlite://overfit-server.db', echo=True)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            
        except Exception as e:
            print(f'[!!] Error opening database: {e}')
    
    def load_matches(self):
        return self.session.query(Match).order_by(Match.top_score)
    
    def save_player(self, new_player):
        self.session.add(new_player)
        self.session.commit()
    
    def save_match(self, winner, loser):
        new_match = Match(winner=winner, loser=loser, timestamp=str(datetime.datetime.now()))
        self.session.add(new_match)
        self.session.commit()
    

"""

self.db = create_engine('sqlite://overfit-server.db', echo=True)
            meta = MetaData()
            player = Table('players', meta,
                               Column('active', Boolean),
                               Column('playing', Boolean),
                               Column('available', Boolean),
                               Column('top_score', Integer),
                               )
            meta.create_all(self.db)
            
            self.db.execute(PLAYER_MODEL)

"""


if __name__ == '__main__':
    pass
