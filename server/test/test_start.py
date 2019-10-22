import unittest
import sys
import os

sys.path.append(os.path.abspath('../src/'))
import start


class TestStart(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(TestStart, self).__init__(*args, **kwargs)
        pass
    
    def test_init(self):
        # set object state
        
        # execute method
        test_start = start.Start()
        # assert expected outcome
        # server and mq are none
        self.assertIsNone(test_start.mq)
        self.assertIsNone(test_start.my_server)

    # def test_server(self):
    #     # set object state
    #     # mock server
    #     # execute method
    #
    #     # assert expected outcome
    #     # server.mq not none
    #     # calls to server set_up, loop
    #     pass


if __name__ == '__main__':
    unittest.main()
