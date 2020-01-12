import sqlite3
from sqlite3 import Error
import sqlalchemy as sql

"""
Defining the player model

create table if not exist overfit_player (
     active  integer,   # 0 or 1
     available integer, # 0 or 1
     playing integer,   # 0 or 1
     top_score integer )

"""

PLAYER_MODEL = 'create table if not exist overfit_player (' \
               'active  integer, ' \
               'available integer, ' \
               'playing integer, ' \
               'top_score integer )'


class Db:
    
    def __init__(self):
        try:
            self.db = sql.create_engine('sqlite://overfit-server.db', echo=True)
            meta = sql.MetaData()
            player = sql.Table('players', meta,
                               sql.Column('active', sql.Boolean),
                               sql.Column('playing', sql.Boolean),
                               sql.Column('available', sql.Boolean),
                               sql.Column('top_score', sql.Integer),
                               )
            meta.create_all(self.db)
            
            self.db.execute(PLAYER_MODEL)
        except Error as e:
            print(f'[!!] Error opening database: {e}')


if __name__ == '__main__':
    pass
