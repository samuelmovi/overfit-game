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
    
    # TODO: workaround server execution during testing
    # def test_init(self):
    #     # set object state
    #
    #     # execute method
    #     test_start = start.Start()
    #     # assert expected outcome
    #     # server and mq are none
    #     self.assertIsNone(test_start.db)
    #     self.assertIsNone(test_start.mq)
    #     self.assertIsNone(test_start.server)
    #
    # def test_now(self):
    #     # set object state
    #     test_start = start.Start()
    #     test_start.mq = Mock()
    #     test_start.db = Mock()
    #     # TODO: inject dependency on server module PullPubServer
    #     # execute method
    #     test_start.now()
    #     # assert results
    #     self.assertIsNotNone(test_start.db)
    #     self.assertIsNotNone(test_start.mq)
    #     self.assertIsNotNone(test_start.server)
    

if __name__ == '__main__':
    unittest.main()
