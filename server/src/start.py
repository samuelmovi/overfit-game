from db_controller import Db
from server import PullPubServer
import zmq_server


class Start:
    
    def __init__(self):
        self.db = None
        self.mq = None
        self.server = None
    
    def now(self):
        # start database
        self.db = Db()
        # create ZMQ connector
        self.mq = zmq_server.ZmqConnector()
        # start server
        self.server = PullPubServer(self.mq, self.db)
        self.server.loop()
        

if __name__ == '__main__':
    start = Start()
    start.now()
