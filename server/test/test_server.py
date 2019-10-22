import unittest
import sys
import os
sys.path.append(os.path.abspath('../src/'))
import server


class TestServer(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(TestServer, self).__init__(*args, **kwargs)
        pass
    
    def test_init(self):
        # set object state
        
        # execute method
        test_server = server.PullPubServer()
        # assert expected outcome
        self.assertIsNone(test_server.mq)
    
    # def test_set_up(self):
    #     # set object state
    #     # mock mq
    #     # mock inner method calls
    #     # execute method
    #
    #     # assert expected outcome
    #     # call to inner method
    #     # call to mq methods
    #     pass
    #
    # def test_connect_pull(self):
    #     # set object state
    #     # mock mq
    #     # execute method
    #
    #     # assert expected outcome
    #     # call to mq method
    #     pass
    #
    # def test_connect_pub(self):
    #     # set object state
    #     # mock mq
    #     # execute method
    #
    #     # assert expected outcome
    #     # call to mq method
    #     pass
    #
    # def test_pull(self):
    #     # set object state
    #     # mock mq pull_receive_multi
    #     # execute method
    #
    #     # assert expected outcome
    #     # mock messages returned
    #     pass
    #
    # def test_pub(self):
    #     # set object state
    #     # mock mq pub_send_multi
    #     # execute method
    #
    #     # assert expected outcome
    #     # call to mq
    #     pass
    #
    # def test_loop(self):
    #     # set object state
    #     # mock inner method calls
    #     # execute method
    #
    #     # assert expected outcome
    #     # call to mq
    #     pass
    
    
if __name__ == '__main__':
    unittest.main()
