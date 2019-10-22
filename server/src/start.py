import zmq_connector
import server


class Start:
    
    def __init__(self):
        self.server = None
        self.mq = None
    
    def server(self):
        self.server = server.PullPubServer()
        self.mq = zmq_connector.ZmqConnector()
        self.server.mq = self.mq
        
        self.server.set_up()
        self.server.loop()


if __name__ == '__main__':
    start = Start()
    start.server()
