import zmq_connector
from controller import Controller
from db_connector import Db
from server import Server


class Start:
    
    def __init__(self):
        # start database
        self.db = Db()
        
        # create ZMQ connector
        self.mq = zmq_connector.ZmqConnector()
        
        # start server
        self.server = Server(self.mq, self.db)
        
        # start controller
        # self.controller = Controller(self.mq)

    # def server(self):
    #     # connector admits host ip in constructor
    #     self.my_server = server.PullPubServer(zmq_connector.ZmqConnector())
    #     # self.my_server.mq = self.mq
    #
    #     self.set_up()
    #     self.my_server.loop()


if __name__ == '__main__':
    start = Start()
