import zmq_connector
import server


class Start:
    
    def __init__(self):
        self.my_server = None
        self.mq = None
    
    def server(self):
        # connector admits host ip in constructor
        self.my_server = server.PullPubServer(zmq_connector.ZmqConnector())
        # self.my_server.mq = self.mq
        
        self.my_server.set_up()
        self.my_server.loop()


if __name__ == '__main__':
    start = Start()
    start.server()
