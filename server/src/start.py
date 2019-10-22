import zmq_connector
import server


class Start:
    
    def __init__(self):
        self.my_server = None
        self.mq = None
    
    def server(self):
        self.my_server = server.PullPubServer()
        self.mq = zmq_connector.ZmqConnector()
        self.my_server.mq = self.mq
        
        self.my_server.set_up()
        self.my_server.loop()


if __name__ == '__main__':
    start = Start()
    start.server()
