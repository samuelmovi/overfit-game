import unittest
import sys
import os
from unittest.mock import Mock

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
        self.assertIsNone(test_start.db)
        self.assertIsNone(test_start.mq)
        self.assertIsNone(test_start.server)
    
    # TODO: find way to mock the imported modules
    # def test_now(self):
    #     # set object state
    #     test_start = start.Start()
    #     # execute method
    #     test_start.now()
    #     # assert results
    #     self.assertIsNotNone(test_start.db)
    #     self.assertIsNotNone(test_start.mq)
    #     self.assertIsNotNone(test_start.server)
    

if __name__ == '__main__':
    unittest.main()
