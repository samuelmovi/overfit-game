
class Controller:
    
    mq = None
    
    def __init__(self, connector=None):
        self.mq = connector
    
    def read_queue(self):
        messages = self.mq.pull_receive_multi()
    
    def parse_command(self):
        # check command in packet and act accordingly
        pass


def loop(self):
    print("[#] starting loop...")
    finished = False
    while not finished:
        try:
            message = self.mq.pull_receive_multi()
            if message is not None:
                print("[#] Message pulled:".format(message))
                # check if user active
                
                
                for part in message:
                    print("\t> {} /{}".format(part, type(part)))
                print("\n[#] rePUBlishing Message...")
                self.pub(message)
        except KeyboardInterrupt:
            finished = True
            

if __name__ == '__main__':
    pass
